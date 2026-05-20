"""NLP service — single embedding model for the entire application lifecycle.

Singleton pattern: ``nlp_service`` is instantiated once at module import and
shared across all requests and the seed pipeline.  Model inference is always
CPU/GPU bound; call the async wrappers from async contexts to avoid blocking
the event loop.

Default model: ``ece-irem/berturk-legal-chunk-retriever``
  - 768-dim output
  - Trained on Turkish legal text for retrieval tasks
  - Compatible with the Vector(768) pgvector columns in case_chunks
"""

from __future__ import annotations

import asyncio
import logging

import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

_DEFAULT_MODEL = "ece-irem/berturk-legal-chunk-retriever"


class NLPService:
    """Async-safe wrapper around SentenceTransformer."""

    def __init__(self, model_name: str = _DEFAULT_MODEL) -> None:
        logger.info("Loading NLP model '%s' …", model_name)
        self._model = SentenceTransformer(model_name)
        logger.info("NLP model ready.")

    # ------------------------------------------------------------------
    # Synchronous core — do NOT call directly from async handlers.
    # ------------------------------------------------------------------

    def get_embedding(self, text: str) -> list[float]:
        """Return a 768-dim L2-normalised vector for a single text."""
        vector: np.ndarray = self._model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return vector.tolist()

    def get_embeddings_batch(
        self,
        texts: list[str],
        batch_size: int = 64,
    ) -> list[list[float]]:
        """Return L2-normalised 768-dim vectors for a list of texts.

        Intended for bulk ingestion in seed scripts where blocking is acceptable.
        """
        vectors: np.ndarray = self._model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=True,
        )
        return vectors.tolist()

    # ------------------------------------------------------------------
    # Async public API
    # ------------------------------------------------------------------

    async def aembed(self, text: str) -> list[float]:
        """Off-thread single-text embedding — safe to await from route handlers."""
        return await asyncio.to_thread(self.get_embedding, text)

    async def aembed_batch(
        self,
        texts: list[str],
        batch_size: int = 64,
    ) -> list[list[float]]:
        """Off-thread batch embedding — safe to await from async contexts."""
        return await asyncio.to_thread(self.get_embeddings_batch, texts, batch_size)


# ---------------------------------------------------------------------------
# Module-level singleton — import and use this everywhere.
#
#   from app.services.nlp_service import nlp_service
#
# Eager-loaded at startup via the lifespan hook in app/main.py:
#   from app.services.nlp_service import nlp_service  # noqa: F401
# ---------------------------------------------------------------------------
nlp_service = NLPService()
