import uuid
from fastapi import APIRouter
from app.schemas.generate import GenerateRequest, GenerateResponse

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


@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    request_id = str(uuid.uuid4())

    # For now return a dummy output (LLM integration comes in next tasks)
    return GenerateResponse(
        request_id=request_id,
        template_id=req.template_id,
        cached=False,
        output=f"Received input: {req.input[:50]}",
    )
