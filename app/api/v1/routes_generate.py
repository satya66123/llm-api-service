import uuid
from fastapi import APIRouter, HTTPException
from app.schemas.generate import GenerateRequest, GenerateResponse
from app.services.prompt_templates import render_prompt

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

    try:
        # Render template prompts (system + user)
        prompts = render_prompt(req.template_id, req.input, req.parameters)

        return GenerateResponse(
            request_id=request_id,
            template_id=req.template_id,
            cached=False,
            output="Prompt template rendered successfully (LLM call next task).",
            system_prompt=prompts["system"],
            user_prompt=prompts["user"],
        )

    except ValueError as ve:
        # Unknown template id, bad input etc.
        raise HTTPException(status_code=400, detail=str(ve))
