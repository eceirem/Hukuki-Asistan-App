from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.api.routes import auth as auth_router
from app.api.routes import search as search_router
from app.api.routes import users as users_router
from app.core.config import settings
from app.db.init import init_db

# Filesystem location of the original court-decision PDFs.  Each row in the
# ``cases`` table stores its filename in ``dosya_adi`` (e.g. ``2018_1055.pdf``).
# We mount the directory below as a static route so the frontend can open the
# document in a new tab via ``http://localhost:8000/pdfs/<dosya_adi>``.
#
# Layout assumed:
#   <backend repo root>/
#     app/
#       main.py        ← this file
#     pdfs/            ← target directory
PDF_DIR: Path = Path(__file__).resolve().parent.parent / "pdfs"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Eager-load the NLP model at startup so the first search request
    # doesn't incur a 30-second cold-start penalty.
    from app.services.nlp_service import nlp_service  # noqa: F401
    await init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router.router)
app.include_router(search_router.router)
app.include_router(users_router.router)

# Serve the raw PDFs.  StaticFiles internally normalises and verifies that the
# requested path stays inside ``PDF_DIR`` (it rejects ``..`` traversal and
# absolute paths), so exposing this without an auth dependency is safe — the
# corpus consists of publicly published Turkish court decisions.
if PDF_DIR.is_dir():
    app.mount("/pdfs", StaticFiles(directory=PDF_DIR), name="pdfs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


class HealthResponse(BaseModel):
    status: str
    project: str


@app.get("/", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", project=settings.PROJECT_NAME)
