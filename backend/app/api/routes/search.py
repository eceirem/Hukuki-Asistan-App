from __future__ import annotations

import asyncio
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import CurrentUser
from app.core.config import settings
from app.crud import crud_case
from app.db.database import get_db
from app.schemas.case import CaseSearchQuery, CaseSearchResult
from app.services.nlp_service import nlp_service
from app.services.xai_service import generate_xai_explanation

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("/", response_model=List[CaseSearchResult])
async def search(
    body: CaseSearchQuery,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: CurrentUser,  # authentication guard — user object not needed in handler
) -> List[CaseSearchResult]:
    # 1. Vectorise the query off the event loop (BERT inference via thread-pool).
    embedding = await nlp_service.aembed(body.query)

    # 2. Hybrid BM25 + cosine search — returns (Case, score, best_chunk_text) tuples.
    hits = await crud_case.search_cases(db, body.query, embedding, body.limit)

    # 3. Optionally generate per-hit XAI explanations in parallel.
    #    Default (ENABLE_LLM_XAI=False): the UI uses ``matched_chunk_text`` as
    #    the retrieval explanation — zero extra latency, fully deterministic.
    if settings.ENABLE_LLM_XAI and hits:
        xai_texts = await asyncio.gather(
            *(generate_xai_explanation(body.query, chunk or "") for _, _, chunk in hits)
        )
    else:
        xai_texts = [None] * len(hits)

    # 4. Build response models from ORM objects.
    return [
        CaseSearchResult.model_validate(case).model_copy(
            update={
                "score": score,
                "matched_chunk_text": chunk,
                "xai_explanation": xai,
            }
        )
        for (case, score, chunk), xai in zip(hits, xai_texts, strict=True)
    ]
