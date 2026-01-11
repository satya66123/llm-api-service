import logging
from openai import OpenAI
from app.core.config import settings

logger = logging.getLogger("llm_client")


class LLMClient:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def generate(self, system_prompt: str, user_prompt: str) -> dict:
        """
        Returns:
        {
          "text": "...",
          "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
        }
        """
        try:
            resp = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )

            text = resp.output_text or ""

            usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
            if getattr(resp, "usage", None):
                usage = {
                    "input_tokens": getattr(resp.usage, "input_tokens", 0) or 0,
                    "output_tokens": getattr(resp.usage, "output_tokens", 0) or 0,
                    "total_tokens": getattr(resp.usage, "total_tokens", 0) or 0,
                }

            return {"text": text, "usage": usage}

        except Exception as e:
            logger.exception("OpenAI generation failed")
            raise RuntimeError(f"OpenAI call failed: {str(e)}") from e


llm_client = LLMClient()
