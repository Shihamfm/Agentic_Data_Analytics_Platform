from analytics_agents.llm.base import LLMProvider
from analytics_agents.models.results import DiscoveryResult


class DataDiscoveryAgent:

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def discover(
        self,
        user_query: str,
    ) -> DiscoveryResult:

        prompt = self._build_prompt(user_query)

        result = await self.llm.generate_structured(
            prompt=prompt,
            response_model=DiscoveryResult,
        )

        return result

    @staticmethod
    def _build_prompt(user_query: str) -> str:

        return f"""
    You are a Data Discovery Agent in an enterprise
    retail demand analytics platform.

    Your job is to understand the user's analytical
    question and identify what data is required to
    answer it.

    Do NOT generate SQL.

    Do NOT invent exact database column names unless
    they are explicitly provided.

    Identify:

    1. The analytical intent.
    2. The business metrics required.
    3. The dimensions needed for analysis.
    4. The filters implied by the question.
    5. The tables or data domains that are likely
    required.

    The system focuses on retail demand forecasting
    and retail analytics.

    Relevant business concepts may include:

    - product
    - SKU
    - store
    - product category
    - brand
    - sales
    - units sold
    - revenue
    - demand
    - inventory
    - stock level
    - stockout
    - promotion
    - discount
    - price
    - sales channel
    - region
    - customer segment
    - date
    - day
    - week
    - month
    - season
    - holiday
    - forecast
    - actual demand
    - forecast error

    The user may ask questions about:

    - historical demand
    - demand trends
    - demand changes
    - product performance
    - store performance
    - category performance
    - inventory
    - promotions
    - pricing
    - demand forecasts
    - forecast accuracy
    - anomalies
    - demand drivers

    User question:

    {user_query}

    Return only the structured discovery result.
    """