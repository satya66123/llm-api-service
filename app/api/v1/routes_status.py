from fastapi import APIRouter
from app.core.config import settings
from app.services.cache import cache
from app.services.prompt_templates import get_templates_list

router = APIRouter(tags=["status"])


@router.get("/status")
def status():
    return {
        "service": settings.APP_NAME,
        "env": settings.APP_ENV,
        "model": settings.OPENAI_MODEL,
        "templates": get_templates_list(),
        "cache_size": cache.size(),
    }
