from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_generate import router as generate_router

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version="2.0.0",
    description="Production-style LLM API service (no RAG, no agents).",
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(generate_router, prefix="/api/v1")
