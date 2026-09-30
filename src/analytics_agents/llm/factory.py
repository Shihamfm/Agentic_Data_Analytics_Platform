from analytics_agents.config.settings import settings
from analytics_agents.llm.base import LLMProvider
from analytics_agents.llm.groq import GroqProvider


def get_llm_provider() -> LLMProvider:

    if settings.llm_provider == "groq":
        return GroqProvider()

    raise ValueError(
        f"Unsupported LLM provider: "
        f"{settings.llm_provider}"
    )