"""CRUD operations for the many-to-many saved_cases association.

All writes go directly to the association table rather than loading the full
ORM relationship, which avoids fetching unnecessary data.

save_case_for_user  — idempotent insert  (ON CONFLICT DO NOTHING)
remove_saved_case   — idempotent delete  (no-op if the row is absent)
get_user_saved_cases — join-based query returning fully hydrated Case objects
"""

from __future__ import annotations

import uuid

from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.association import saved_cases as saved_cases_table
from app.models.case import Case


async def save_case_for_user(
    db: AsyncSession,
    user_id: uuid.UUID,
    case_id: int,
) -> None:
    """Bookmark *case_id* for *user_id*.  Duplicate saves are silently ignored."""
    stmt = (
        pg_insert(saved_cases_table)
        .values(user_id=user_id, case_id=case_id)
        .on_conflict_do_nothing()
    )
    await db.execute(stmt)
    await db.commit()


async def remove_saved_case(
    db: AsyncSession,
    user_id: uuid.UUID,
    case_id: int,
) -> None:
    """Remove the bookmark.  No-op if the record does not exist."""
    stmt = delete(saved_cases_table).where(
        and_(
            saved_cases_table.c.user_id == user_id,
            saved_cases_table.c.case_id == case_id,
        )
    )
    await db.execute(stmt)
    await db.commit()


async def get_user_saved_cases(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> list[Case]:
    """Return all Cases bookmarked by *user_id*, ordered by case id asc."""
    result = await db.execute(
        select(Case)
        .join(saved_cases_table, Case.id == saved_cases_table.c.case_id)
        .where(saved_cases_table.c.user_id == user_id)
        .order_by(Case.id)
    )
    return list(result.scalars().all())
