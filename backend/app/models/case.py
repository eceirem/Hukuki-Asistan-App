from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Date, DateTime, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.association import saved_cases as saved_cases_table

if TYPE_CHECKING:
    from app.models.user import User


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # --- File identifier (matches `file_name` in JSON / `id` in CSV) ---
    dosya_adi: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    # --- Legal identifiers ---
    esas_no: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    karar_no: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # --- Case metadata ---
    mahkeme: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    dava_konusu: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    dava_tarihi: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    karar_tarihi: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # --- Summaries (display only — not used in any search index) ---
    sum_human: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sum_model: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- Judicial breakdown (display only — rendered in CaseDetailModal sections) ---
    # Sourced from cases_data.json root-level keys (tam_olay / gerekce / hukum)
    # with rrl_segments.{facts_text,reasoning_text,verdict_text} as fallback.
    tam_olay: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    gerekce: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hukum: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- BM25 full-text search index ---
    # Stores the concatenated olay (facts) + gerekçe (reasoning) + karar (verdict)
    # text of the case as a TSVECTOR for Turkish FTS (ts_rank / plainto_tsquery).
    # Populated by seed_data.py via to_tsvector aggregated from case_chunks.chunk_text.
    olay_gerekce_karar: Mapped[Optional[str]] = mapped_column(TSVECTOR, nullable=True)

    # --- Audit ---
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    saved_by_users: Mapped[List["User"]] = relationship(
        "User",
        secondary=saved_cases_table,
        back_populates="saved_cases",
        lazy="selectin",
    )

    chunks: Mapped[List["CaseChunk"]] = relationship(
        "CaseChunk",
        back_populates="case",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    __table_args__ = (
        UniqueConstraint("esas_no", "karar_no", name="uix_esas_karar"),
        Index(
            "ix_cases_olay_gerekce_karar_gin",
            "olay_gerekce_karar",
            postgresql_using="gin",
        ),
    )


class CaseChunk(Base):
    __tablename__ = "case_chunks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    case_id: Mapped[int] = mapped_column(
        ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True
    )
    chunk_id: Mapped[str] = mapped_column(String(255), nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(768), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    case: Mapped["Case"] = relationship("Case", back_populates="chunks", lazy="noload")

    __table_args__ = (
        Index(
            "ix_case_chunks_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )
