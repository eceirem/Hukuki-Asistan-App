"""Idempotent database bootstrap for the Hukukî Asistan data layer.

Runs in two ordered passes:

1.  Required PostgreSQL extensions (``vector`` for pgvector, ``pg_trgm`` for
    trigram similarity).
2.  ``Base.metadata.create_all`` — creates every ORM table registered on the
    declarative ``Base`` (User, Case, CaseChunk, saved_cases).

Note on ``cases.olay_gerekce_karar`` (TSVECTOR)
────────────────────────────────────────────────
This column is populated by ``seed_data.py`` after all CaseChunk rows have been
inserted, using an aggregated ``to_tsvector`` over the chunk texts:

    UPDATE cases c
    SET olay_gerekce_karar = sub.tsvec
    FROM (
        SELECT case_id,
               to_tsvector('turkish', string_agg(chunk_text, ' ')) AS tsvec
        FROM case_chunks
        GROUP BY case_id
    ) sub
    WHERE c.id = sub.case_id;

No trigger is installed here because the source text columns (olay, gerekçe,
karar) are not stored as individual columns on the ``cases`` table — their
content lives in ``case_chunks``.

In production this responsibility should move to Alembic migrations.
"""

from __future__ import annotations

import asyncio
import logging

from sqlalchemy import text

import app.models  # noqa: F401  -- side-effect: runs models/__init__.py
from app.models.case import Case, CaseChunk  # noqa: F401  -- explicit registration on Base.metadata
from app.models.user import User  # noqa: F401
from app.db.database import Base, engine

logger = logging.getLogger(__name__)


_EXTENSIONS: tuple[str, ...] = (
    "CREATE EXTENSION IF NOT EXISTS vector",
    "CREATE EXTENSION IF NOT EXISTS pg_trgm",
)


async def init_db() -> None:
    """Bootstrap extensions and tables."""
    async with engine.begin() as conn:
        for ddl in _EXTENSIONS:
            await conn.execute(text(ddl))

        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database initialised: extensions and tables ready.")


async def drop_db() -> None:
    """Drop all ORM tables. Destructive."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    logger.info("Database dropped: all tables removed.")


async def reset_db() -> None:
    """Drop everything, then recreate from scratch. Destructive."""
    await drop_db()
    await init_db()


def _main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-7s  %(name)s — %(message)s",
    )
    asyncio.run(reset_db())


if __name__ == "__main__":
    _main()
