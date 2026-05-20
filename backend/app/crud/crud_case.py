"""CRUD operations for the Case model.

Two-Stage Rerank Pipeline
─────────────────────────
Stage 1 — BM25L Retrieval
    Full-text search on ``cases.olay_gerekce_karar`` (TSVECTOR).  We build an
    *OR*-joined ``to_tsquery`` from the user's free text and rank candidates
    with ``ts_rank``.  Why OR and not ``plainto_tsquery``?  ``plainto_tsquery``
    AND-joins every stem; the Turkish snowball stemmer is inconsistent across
    morphologically related forms (``mesajlarıyla`` and ``mesajlaşmalarının``
    stem differently) and a 4–5 token query almost always produces an empty
    intersection.  OR semantics + ``ts_rank`` give us a relevance-ordered
    candidate pool instead of an all-or-nothing match.  Returns the top
    *bm25_candidates* (default 100) case IDs.

Stage 2 — Dense Reranking
    Vectorise the query via ``nlp_service`` (same model used at index time).
    Restrict the pgvector cosine search to chunks belonging to the Stage-1
    candidates only.  Per case, keep the minimum cosine distance (best chunk)
    AND the verbatim text of that chunk — the latter feeds the
    "Neden bu karar getirildi?" XAI panel.

Both stages live in a single SQL statement built from CTEs, so they run in
one round-trip and share one snapshot — no temporary tables, no commit/flush
lifecycle concerns under ``AsyncSession``.

Result
    Cases ranked by best-chunk cosine similarity (descending), top *top_k*.
    Each row carries ``(Case, similarity_score, best_chunk_text)``.
"""

from __future__ import annotations

import re

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case, CaseChunk


# Tokens for to_tsquery: split on whitespace and on characters that have
# special meaning inside a tsquery (``& | ! < > ( ) : * ' "``).  Everything
# else (including Turkish diacritics) is preserved; ``to_tsquery('turkish', …)``
# will lowercase and stem these tokens with the same snowball stemmer used
# by ``to_tsvector`` at seed time, so lexemes line up correctly.
_TSQUERY_TOKEN_SPLIT = re.compile(r"[\s|&!<>():'\"*]+")


def _build_or_tsquery_text(query_text: str) -> str | None:
    """Convert free text into an OR-joined ``to_tsquery`` argument.

    Returns ``None`` when the query has no usable tokens (empty / whitespace /
    only-operators) — callers should short-circuit in that case.
    """
    tokens = [tok for tok in _TSQUERY_TOKEN_SPLIT.split(query_text) if tok]
    if not tokens:
        return None
    return " | ".join(tokens)


async def search_cases(
    db: AsyncSession,
    query_text: str,
    embedding: list[float],
    top_k: int = 10,
    bm25_candidates: int = 100,
) -> list[tuple[Case, float, str | None]]:
    """Return up to *top_k* ``(Case, cosine_similarity, best_chunk_text)`` tuples.

    Args:
        db:               Async SQLAlchemy session.
        query_text:       Raw query string for BM25 Stage 1.
        embedding:        768-dim query vector for dense Stage 2.
        top_k:            Maximum results to return.
        bm25_candidates:  Number of BM25 candidates passed to Stage 2.
    """
    or_query_text = _build_or_tsquery_text(query_text)
    if or_query_text is None:
        return []

    tsquery = func.to_tsquery("turkish", or_query_text)
    bm25_rank = func.ts_rank(Case.olay_gerekce_karar, tsquery)

    # ── Stage 1: BM25L retrieval ─────────────────────────────────────────────
    # Top-N case IDs whose TSVECTOR matches ANY stem, ordered by ts_rank.
    bm25_cte = (
        select(
            Case.id.label("case_id"),
            bm25_rank.label("bm25_rank"),
        )
        .where(Case.olay_gerekce_karar.op("@@")(tsquery))
        .order_by(bm25_rank.desc())
        .limit(bm25_candidates)
        .cte("bm25_candidates")
    )

    # ── Stage 2: Dense reranking ─────────────────────────────────────────────
    # For each Stage-1 candidate case, pick the SINGLE chunk with the lowest
    # cosine distance to the query embedding.  DISTINCT ON keeps the row with
    # the best distance per case_id while preserving the chunk_id/chunk_text.
    chunk_distance = CaseChunk.embedding.cosine_distance(embedding)
    best_chunk_cte = (
        select(
            CaseChunk.case_id,
            CaseChunk.chunk_text.label("chunk_text"),
            chunk_distance.label("cosine_dist"),
        )
        .where(CaseChunk.case_id.in_(select(bm25_cte.c.case_id)))
        .distinct(CaseChunk.case_id)
        .order_by(CaseChunk.case_id, chunk_distance.asc())
        .cte("best_chunk_per_case")
    )

    # ── Final result ─────────────────────────────────────────────────────────
    # Cosine similarity = 1 − cosine distance (unit-norm vectors → [0, 1]).
    cosine_similarity = (1.0 - best_chunk_cte.c.cosine_dist).label("score")

    stmt = (
        select(Case, cosine_similarity, best_chunk_cte.c.chunk_text)
        .join(best_chunk_cte, best_chunk_cte.c.case_id == Case.id)
        .order_by(best_chunk_cte.c.cosine_dist)  # ascending distance = descending similarity
        .limit(top_k)
    )

    rows = (await db.execute(stmt)).all()
    return [(row[0], float(row[1]), row[2]) for row in rows]
