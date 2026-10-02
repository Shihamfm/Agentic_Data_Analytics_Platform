import json

import pandas as pd

from analytics_agents.llm.base import LLMProvider
from analytics_agents.models.results import (
    AnalysisResult,
    VisualizationResult,
)


class VisualizationAgent:

    def __init__(
        self,
        llm: LLMProvider,
    ):
        self.llm = llm

    async def create_specs(
        self,
        dataframe: pd.DataFrame,
        analysis: AnalysisResult,
        user_query: str,
    ) -> VisualizationResult:

        prompt = self._build_prompt(
            dataframe=dataframe,
            analysis=analysis,
            user_query=user_query,
        )

        return await self.llm.generate_structured(
            prompt=prompt,
            response_model=VisualizationResult,
        )

    @staticmethod
    def _build_prompt(
        dataframe: pd.DataFrame,
        analysis: AnalysisResult,
        user_query: str,
    ) -> str:

        columns = list(
            dataframe.columns
        )

        sample = (
            dataframe
            .head(10)
            .to_dict(
                orient="records"
            )
        )

        return f"""
You are the Visualization Agent in a retail
analytics platform.

Determine the most useful visualizations for
the user's analytical question.

User question:

{user_query}

Available columns:

{json.dumps(columns, indent=2)}

Sample data:

{json.dumps(
    sample,
    indent=2,
    default=str,
)}

Analysis:

{analysis.model_dump_json(indent=2)}

Choose appropriate chart types.

Supported chart types:

- line
- bar
- scatter
- histogram
- area

Rules:

1. Only use columns that exist in the data.
2. Do not invent columns.
3. Do not create unnecessary charts.
4. Prefer one clear chart over many redundant charts.
5. Use line charts for time-series trends.
6. Use bar charts for category/store/product comparisons.
7. Use scatter charts for relationships between
   numerical variables.
8. Use histograms for distributions.
9. Keep chart titles business-friendly.

Return only the visualization specification.
"""