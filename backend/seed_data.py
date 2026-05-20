"""Full database reset and seed script.

Usage:
    uv run python seed_data.py

Steps:
  1. Drop all tables and recreate from the current ORM schema.
  2. Read `cases_data.json` and populate the `cases` table.
  3. Read `chunks_data.csv` (columns: id, chunk_id, chunk_text), batch-encode
     chunk texts via the centralised NLP service, and insert into `case_chunks`.
  4. Build the `cases.olay_gerekce_karar` TSVECTOR for each case by aggregating
     its chunk texts with ``to_tsvector('turkish', ...)``.

The NLP service (``ece-irem/berturk-legal-chunk-retriever``) is loaded via the
application singleton ``nlp_service`` — the same instance used at query time.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import sys
from datetime import date, datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import select, text

# ---------------------------------------------------------------------------
# Bootstrap: ensure the package root is on sys.path so `app.*` imports work
# when the script is executed directly (not as a module).
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.database import AsyncSessionLocal, Base, engine  # noqa: E402
import app.models  # noqa: F401, E402  -- registers all models on Base.metadata
from app.models.case import Case, CaseChunk  # noqa: E402
from app.services.nlp_service import nlp_service  # noqa: E402  -- loads model singleton

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

CASES_JSON = ROOT / "cases_data.json"
CHUNKS_CSV = ROOT / "chunks_data.csv"
EMBED_BATCH_SIZE = 64


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DATE_PATTERN = re.compile(r"\b(\d{1,2}[./]\d{1,2}[./]\d{4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b")

def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    match = _DATE_PATTERN.search(value)
    cleaned = match.group(1) if match else value.strip()
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(cleaned, fmt).date()
        except (ValueError, AttributeError):
            continue
    logger.warning("Could not parse date value: %r — storing NULL", value)
    return None


# ---------------------------------------------------------------------------
# Step 1: Reset database
# ---------------------------------------------------------------------------

async def reset_db() -> None:
    logger.info("Dropping all tables …")
    async with engine.begin() as conn:
        # Remove the FTS trigger/function if they exist from a previous schema.
        await conn.execute(text("DROP TRIGGER IF EXISTS trg_cases_fts_update ON cases"))
        await conn.execute(text("DROP FUNCTION IF EXISTS cases_fts_update()"))
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("All tables dropped.")

    logger.info("Creating tables from current ORM schema …")
    async with engine.begin() as conn:
        for ddl in (
            "CREATE EXTENSION IF NOT EXISTS vector",
            "CREATE EXTENSION IF NOT EXISTS pg_trgm",
        ):
            await conn.execute(text(ddl))
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Schema ready.")


# ---------------------------------------------------------------------------
# Step 2: Seed cases from JSON
# ---------------------------------------------------------------------------

import pandas as pd

async def seed_cases(db_cases: list[dict]) -> dict[str, int]:
    """Insert Case rows; return {dosya_adi: pk_id} mapping for chunk linking."""
    logger.info("Inserting %d cases …", len(db_cases))

    # --- YENİ EKLENEN KISIM: CSV'den konu başlıklarını çekme ---
    konu_mapping = {}
    try:
        # Sadece id ve konu sütunlarını okuyoruz (bellek ve hız tasarrufu için)
        df_konu = pd.read_csv(CHUNKS_CSV, usecols=["id", "category"], dtype=str).fillna("")
        
        # 'id' (dosya adı) ile 'konu' eşleşmesini bir sözlüğe (dict) çeviriyoruz
        # zip() metodu ile: {"2018_1055.pdf": "Tazminat", ...} şeklinde bir yapı oluşur
        konu_mapping = dict(zip(df_konu["id"], df_konu["category"]))
        logger.info("CSV'den %d benzersiz dosya için konu başlığı alındı.", len(konu_mapping))
    except Exception as e:
        logger.error("CSV'den konu başlıkları okunurken hata: %s", e)

    async with AsyncSessionLocal() as session:
        for data in db_cases:
            dosya_adi = data.get("dosya_adi")

            if not dosya_adi:
                logger.warning(f"Atlanan Kayıt: Dosya adı (id) bulunamadı. JSON verisi: {data.get('esas_no')}")
                continue

            csv_konu = konu_mapping.get(dosya_adi)
            final_konu = csv_konu if csv_konu else data.get("dava_konusu")

            session.add(Case(
                dosya_adi=dosya_adi,
                esas_no=data.get("esas_no") or None,
                karar_no=data.get("karar_no") or None,
                mahkeme=data.get("mahkeme") or None,
                dava_konusu=final_konu or None,
                dava_tarihi=data.get("dava_tarihi"),
                karar_tarihi=data.get("karar_tarihi"),
                sum_human=data.get("sum_human") or None,
                sum_model=data.get("sum_model") or None,
                tam_olay=data.get("tam_olay") or None,
                gerekce=data.get("gerekce") or None,
                hukum=data.get("hukum") or None,
            ))

        await session.flush()

        result = await session.execute(select(Case.id, Case.dosya_adi))
        dosya_to_id: dict[str, int] = {
            dosya_adi: pk
            for pk, dosya_adi in result.all()
            if dosya_adi
        }

        await session.commit()

    logger.info("Cases inserted. %d dosya_adi→id mappings collected.", len(dosya_to_id))
    return dosya_to_id

# ---------------------------------------------------------------------------
# Step 3: Seed chunks with embeddings (via centralised NLP service)
# ---------------------------------------------------------------------------

async def seed_chunks(dosya_to_id: dict[str, int]) -> None:
    df = pd.read_csv(CHUNKS_CSV, dtype=str).fillna("")

    # Normalise column name: CSV uses "strategy_chunked" for the chunk text.
    if "strategy_chunked" in df.columns and "chunk_text" not in df.columns:
        df.rename(columns={"strategy_chunked": "chunk_text"}, inplace=True)

    required = {"id", "chunk_id", "chunk_text"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"chunks_data.csv is missing columns: {missing}")

    total = len(df)
    logger.info("Batch-encoding %d chunk texts …", total)

    # Use the application singleton — same model used at query time.
    embeddings: list[list[float]] = await asyncio.to_thread(
        nlp_service.get_embeddings_batch,
        df["chunk_text"].tolist(),
        EMBED_BATCH_SIZE,
    )

    chunks: list[CaseChunk] = []
    skipped = 0
    for i, row in df.iterrows():
        case_pk = dosya_to_id.get(row["id"])
        if case_pk is None:
            logger.debug(
                "No Case found for dosya_adi=%r — skipping chunk %r",
                row["id"], row["chunk_id"],
            )
            skipped += 1
            continue

        chunks.append(CaseChunk(
            case_id=case_pk,
            chunk_id=row["chunk_id"] or None,
            chunk_text=row["chunk_text"] or None,
            embedding=embeddings[i],
        ))

    if skipped:
        logger.warning("Skipped %d chunks with no matching Case.", skipped)

    async with AsyncSessionLocal() as session:
        session.add_all(chunks)
        await session.commit()

    logger.info("Inserted %d chunks.", len(chunks))


# ---------------------------------------------------------------------------
# Step 4: Build olay_gerekce_karar TSVECTOR from chunk texts
# ---------------------------------------------------------------------------

async def build_tsvectors() -> None:
    """Aggregate each case's chunk texts into its olay_gerekce_karar TSVECTOR."""
    logger.info("Building olay_gerekce_karar TSVECTORs from chunk texts …")
    async with engine.begin() as conn:
        await conn.execute(text("""
            UPDATE cases c
            SET olay_gerekce_karar = sub.tsvec
            FROM (
                SELECT
                    case_id,
                    to_tsvector('turkish', string_agg(chunk_text, ' ')) AS tsvec
                FROM case_chunks
                GROUP BY case_id
            ) sub
            WHERE c.id = sub.case_id
        """))
    logger.info("TSVECTORs built.")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

async def main() -> None:
    if not CASES_JSON.exists():
        logger.error("cases_data.json not found at %s", CASES_JSON)
        sys.exit(1)
    if not CHUNKS_CSV.exists():
        logger.error("chunks_data.csv not found at %s", CHUNKS_CSV)
        sys.exit(1)

    # 1. Reset DB
    await reset_db()

    # 2. Parse JSON → Case dicts
    logger.info("Reading %s …", CASES_JSON)
    with CASES_JSON.open(encoding="utf-8") as fh:
        raw: list[dict] = json.load(fh)

    db_cases: list[dict] = []
    for entry in raw:
        meta = entry.get("meta_data", {}) or {}
        # rrl_segments holds the canonical English-keyed judicial breakdown.
        # Some entries also expose a Turkish-keyed copy at the root level
        # (tam_olay / gerekce / hukum) — prefer the root keys when present,
        # otherwise fall back to rrl_segments.{facts_text,reasoning_text,verdict_text}.
        rrl = entry.get("rrl_segments", {}) or {}
        db_cases.append({
            "dosya_adi":    meta.get("file_name") or None,
            "esas_no":      meta.get("esas_no") or None,
            "karar_no":     meta.get("karar_no") or None,
            "mahkeme":      meta.get("court_name") or None,
            "dava_konusu":  meta.get("dava_konusu") or None,
            "dava_tarihi":  _parse_date(meta.get("dava_tarihi")),
            "karar_tarihi": _parse_date(meta.get("karar_tarihi")),
            "sum_human":    entry.get("summary_for_human") or None,
            "sum_model":    entry.get("summary_for_model") or None,
            "tam_olay":     entry.get("tam_olay") or rrl.get("facts_text") or None,
            "gerekce":      entry.get("gerekce") or rrl.get("reasoning_text") or None,
            "hukum":        entry.get("hukum") or rrl.get("verdict_text") or None,
        })

    # Deduplicate by dosya_adi (last entry wins).
    by_dosya: dict[str, dict] = {}
    for case in db_cases:
        key = case["dosya_adi"] or str(id(case))
        by_dosya[key] = case
    db_cases = list(by_dosya.values())

    # Composite unique constraint: (esas_no, karar_no) ikilisi Türk hukuk
    # sisteminde benzersiz sayılır. Tekrar eden ikilide karar_no'yu NULL yap.
    seen_esas_karar: set[tuple[str | None, str | None]] = set()
    for case in db_cases:
        if case["esas_no"] and case["karar_no"]:
            key = (case["esas_no"], case["karar_no"])
            if key in seen_esas_karar:
                case["karar_no"] = None
            else:
                seen_esas_karar.add(key)

    # 3. Seed cases
    dosya_to_id = await seed_cases(db_cases)

    # 4. Seed chunks with embeddings (NLP service already loaded as singleton)
    await seed_chunks(dosya_to_id)

    # 5. Build BM25 TSVECTOR index from chunk texts
    await build_tsvectors()

    logger.info("All done.")


if __name__ == "__main__":
    asyncio.run(main())
