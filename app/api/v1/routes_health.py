from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok", "service": settings.APP_NAME, "env": settings.APP_ENV}
