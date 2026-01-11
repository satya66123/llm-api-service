import uuid
from fastapi import APIRouter, HTTPException
from app.schemas.generate import GenerateRequest, GenerateResponse
from app.services.prompt_templates import render_prompt
from app.services.llm_client import llm_client
from app.services.cache import cache

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
        # Render prompt template
        prompts = render_prompt(req.template_id, req.input, req.parameters)

        # Cache key
        cache_key = cache.make_key(req.template_id, req.input, req.parameters)

        # Cache hit
        cached_value = cache.get(cache_key)
        if cached_value:
            return GenerateResponse(
                request_id=request_id,
                template_id=req.template_id,
                cached=True,
                input_tokens=cached_value.get("input_tokens", 0),
                output_tokens=cached_value.get("output_tokens", 0),
                total_tokens=cached_value.get("total_tokens", 0),
                output=cached_value.get("output", ""),
                system_prompt=prompts["system"],
                user_prompt=prompts["user"],
            )

        # Cache miss -> OpenAI call
        result = llm_client.generate(prompts["system"], prompts["user"])
        usage = result.get("usage", {}) or {}
        output_text = result.get("text", "") or ""

        response_payload = {
            "output": output_text,
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }

        # Store in cache
        cache.set(cache_key, response_payload)

        return GenerateResponse(
            request_id=request_id,
            template_id=req.template_id,
            cached=False,
            input_tokens=response_payload["input_tokens"],
            output_tokens=response_payload["output_tokens"],
            total_tokens=response_payload["total_tokens"],
            output=response_payload["output"],
            system_prompt=prompts["system"],
            user_prompt=prompts["user"],
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail={"error": "BadRequest", "details": str(ve)},
        )

    except RuntimeError as re:
        raise HTTPException(
            status_code=502,
            detail={"error": "LLMProviderError", "details": str(re)},
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "InternalServerError", "details": str(e)},
        )
