import json
from typing import TypeVar

from groq import AsyncGroq
from pydantic import BaseModel

from analytics_agents.config.settings import settings
from analytics_agents.llm.base import LLMProvider


T = TypeVar("T", bound=BaseModel)


class GroqProvider(LLMProvider):

    def __init__(self):
        if not settings.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = AsyncGroq(
            api_key = settings.groq_api_key
        )

        self.model = settings.llm_model

    async def generate(
        self,
        prompt: str,
    ) -> str:
        """Generate plain text using LangChain's async invoke."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""

    async def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:

        schema = response_model.model_json_schema()

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Return only valid JSON matching "
                        "the provided JSON schema."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"{prompt}\n\n"
                        f"JSON schema:\n"
                        f"{json.dumps(schema)}"
                    ),
                },
            ],
            response_format={
                "type": "json_object"
            },
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError(
                "Groq returned an empty response."
            )

        return response_model.model_validate_json(content)