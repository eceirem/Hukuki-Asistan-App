from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

saved_cases = Table(
    "saved_cases",
    Base.metadata,
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "case_id",
        Integer,
        ForeignKey("cases.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
