from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "Hukuki Asistan"

    # CORS — comma-separated list of allowed origins.
    # Development default: the Vite dev server.
    # Production: set to your actual frontend domain, e.g. https://hukuki.example.com
    CORS_ALLOWED_ORIGINS: str = "http://localhost:5173"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Database (must match the asyncpg DSN format)
    DATABASE_URL: str

    # ── Explainability ─────────────────────────────────────────────────────
    # Toggle for LLM-powered "Neden bu karar getirildi?" generation.
    #   OFF (default) → backend returns the best-matching chunk text verbatim;
    #                   the UI uses it as the retrieval explanation.
    #   ON            → backend calls xai_service.generate_xai_explanation which
    #                   hits the OpenRouter API (OpenAI-compatible).
    ENABLE_LLM_XAI: bool = False

    # ── OpenRouter (XAI provider) ───────────────────────────────────────────
    # Only used when ENABLE_LLM_XAI=True.
    LLM_API_URL: str = "https://openrouter.ai/api/v1"
    LLM_API_TOKEN: str = ""
    LLM_MODEL_NAME: str = "meta-llama/llama-3.2-3b-instruct"


settings = Settings()
