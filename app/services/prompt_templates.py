from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class PromptTemplate:
    template_id: str
    system: str
    user: str


TEMPLATES: Dict[str, PromptTemplate] = {
    "basic_chat_v1": PromptTemplate(
        template_id="basic_chat_v1",
        system="You are a helpful assistant. Follow instructions carefully.",
        user="User Input: {input}\nTone: {tone}",
    ),
    "summarize_v1": PromptTemplate(
        template_id="summarize_v1",
        system="You are an expert summarizer. Be concise and accurate.",
        user="Summarize the following text:\n\n{input}",
    ),
}


def get_templates_list() -> list[str]:
    return list(TEMPLATES.keys())


def render_prompt(template_id: str, user_input: str, parameters: Dict[str, Any]) -> Dict[str, str]:
    """
    Returns:
      { "system": "...", "user": "..." }
    """
    if template_id not in TEMPLATES:
        raise ValueError(f"Unknown template_id: {template_id}. Available: {get_templates_list()}")

    tpl = TEMPLATES[template_id]
    params = parameters or {}

    # safe defaults
    tone = params.get("tone", "neutral")

    user_prompt = tpl.user.format(input=user_input, tone=tone)

    return {"system": tpl.system, "user": user_prompt}
