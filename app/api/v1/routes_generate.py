from fastapi import APIRouter

router = APIRouter(tags=["generate"])


@router.get("/generate")
def generate_info():
    return {
        "message": "Use POST /api/v1/generate",
        "example": {
            "template_id": "basic_chat_v1",
            "input": "Explain FastAPI in simple words",
            "parameters": {"tone": "simple"},
        },
    }


@router.post("/generate")
def generate():
    return {"message": "generate endpoint ready (implementation next task)"}
