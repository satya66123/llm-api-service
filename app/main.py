from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version="2.0.0",
    description="Production-style LLM API service (no RAG, no agents).",
)


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "service": settings.APP_NAME, "env": settings.APP_ENV}
