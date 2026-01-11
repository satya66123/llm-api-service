import uuid
from fastapi import APIRouter, HTTPException
from app.schemas.generate import GenerateRequest, GenerateResponse
from app.services.prompt_templates import render_prompt
from app.services.llm_client import llm_client

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
        # 1) Render prompt template (system + user)
        prompts = render_prompt(req.template_id, req.input, req.parameters)

        # 2) Call OpenAI Responses API
        result = llm_client.generate(prompts["system"], prompts["user"])

        usage = result.get("usage", {}) or {}
        output_text = result.get("text", "") or ""

        return GenerateResponse(
            request_id=request_id,
            template_id=req.template_id,
            cached=False,
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            output=output_text,
            system_prompt=prompts["system"],
            user_prompt=prompts["user"],
        )

    except ValueError as ve:
        # Template validation error etc.
        raise HTTPException(status_code=400, detail=str(ve))

    except RuntimeError as re:
        # OpenAI call failure
        raise HTTPException(status_code=502, detail=str(re))

    except Exception as e:
        # Unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
