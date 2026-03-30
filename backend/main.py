import os
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.database import create_tables
from backend.routers import documents, analysis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Blueprint QA API — creating tables if needed...")
    await create_tables()
    yield
    logger.info("Shutting down Blueprint QA API.")


app = FastAPI(title="Blueprint QA API", version="1.0.0", lifespan=lifespan)

_extra_origins = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        *_extra_origins,
    ],
    allow_origin_regex=r"https://(.*\.onrender\.com|.*\.vercel\.app)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(analysis.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


# Serve the SvelteKit static build (placed here by Dockerfile)
_static = Path(__file__).parent / "static"

if _static.is_dir():
    # Serve immutable assets with StaticFiles (efficient, proper cache headers)
    _app_assets = _static / "_app"
    if _app_assets.is_dir():
        app.mount("/_app", StaticFiles(directory=str(_app_assets)), name="assets")

    @app.get("/{full_path:path}")
    async def spa_fallback(full_path: str):
        """Serve static files or fall back to the SPA entry point."""
        candidate = _static / full_path
        if candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(_static / "200.html")
