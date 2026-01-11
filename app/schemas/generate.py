from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class GenerateRequest(BaseModel):
    template_id: str = Field(..., min_length=3, max_length=64)
    input: str = Field(..., min_length=1, max_length=5000)
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)


class GenerateResponse(BaseModel):
    request_id: str
    template_id: str
    cached: bool
    output: str
    system_prompt: str
    user_prompt: str
