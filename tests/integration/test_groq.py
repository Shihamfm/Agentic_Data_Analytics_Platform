import pytest

from analytics_agents.llm.factory import get_llm_provider


@pytest.mark.asyncio
async def test_groq_provider():

    llm = get_llm_provider()

    response = await llm.generate(
        "Explain what a data warehouse is in one sentence."
    )

    assert isinstance(response, str)
    assert len(response) > 0