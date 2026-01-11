import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_generate import router as generate_router
from app.api.v1.routes_status import router as status_router

setup_logging()
logger = logging.getLogger("main")

app = FastAPI(
    title=settings.APP_NAME,
    version="2.0.0",
    description="Production-style LLM API service (no RAG, no agents).",
)

# Routers
app.include_router(health_router, prefix="/api/v1")
app.include_router(generate_router, prefix="/api/v1")
app.include_router(status_router, prefix="/api/v1")


# Global exception handler (fallback safety)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "InternalServerError", "details": "Unexpected server error occurred"},
    )
