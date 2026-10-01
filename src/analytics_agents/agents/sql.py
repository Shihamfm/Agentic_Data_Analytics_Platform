from analytics_agents.data.catalog import RETAIL_CATALOG
from analytics_agents.llm.base import LLMProvider
from analytics_agents.models.results import (
    DiscoveryResult,
    SQLResult,
)

class SQLGenerationAgent:

    def __init__(
        self,
        llm: LLMProvider,
    ):
        self.llm = llm

    async def generate(
        self,
        discovery: DiscoveryResult,
    ) -> SQLResult:

        prompt = self._build_prompt(discovery)

        return await self.llm.generate_structured(
            prompt=prompt,
            response_model=SQLResult,
        )

    @staticmethod
    def _build_prompt(
        discovery: DiscoveryResult,
    ) -> str:

        catalog = RETAIL_CATALOG.model_dump_json(
            indent=2
        )

        discovery_json = discovery.model_dump_json(
            indent=2
        )

        return f"""
You are a SQL Generation Agent in a retail
analytics platform.

Your task is to generate SQL that answers the
analytical requirements identified by the Data
Discovery Agent.

You MUST use the provided semantic catalog.

Do NOT invent:

- tables
- columns
- metrics
- dimensions

Use only fields that exist in the semantic catalog.

The SQL must be:

- read-only
- deterministic
- analytically meaningful
- compatible with Databricks SQL

Do NOT execute the SQL.

Do NOT modify any data.

Do NOT use:

- INSERT
- UPDATE
- DELETE
- MERGE
- DROP
- ALTER
- CREATE
- TRUNCATE

Semantic catalog:

{catalog}

Discovery result:

{discovery_json}

Generate the SQL required to answer the discovery
requirements.

Return the SQL and explain briefly what it does.
"""