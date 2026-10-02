import json

import pandas as pd

from analytics_agents.llm.base import LLMProvider
from analytics_agents.models.results import (
    AnalysisResult,
)
from analytics_agents.tools.retail_analysis import (
    calculate_category_performance,
    calculate_monthly_demand,
    calculate_product_performance,
    calculate_store_performance,
    calculate_summary_metrics,
)
from analytics_agents.tools.statistical_analysis import (
    RetailStatisticalAnalyzer,
)


class RetailAnalysisAgent:

    def __init__(
        self,
        llm: LLMProvider,
    ):
        self.llm = llm

    async def analyze(
        self,
        dataframe: pd.DataFrame,
        user_query: str,
    ) -> AnalysisResult:

        evidence = self._build_evidence(
            dataframe
        )

        prompt = self._build_prompt(
            user_query=user_query,
            evidence=evidence,
        )

        return await self.llm.generate_structured(
            prompt=prompt,
            response_model=AnalysisResult,
        )

    @staticmethod
    def _build_evidence(
        dataframe: pd.DataFrame,
    ) -> dict:

        category_performance = (
            calculate_category_performance(
                dataframe
            )
        )

        store_performance = (
            calculate_store_performance(
                dataframe
            )
        )

        product_performance = (
            calculate_product_performance(
                dataframe
            )
        )

        monthly_demand = (
            calculate_monthly_demand(
                dataframe
            )
        )

        statistical_analyzer = (
        RetailStatisticalAnalyzer()
        )

        statistical_results = (
            statistical_analyzer.analyze(
                dataframe
                )
            )

        return {
            "summary_metrics": (
                calculate_summary_metrics(
                    dataframe
                )
            ),
            "category_performance": (
                category_performance
                .to_dict(orient="records")
            ),
            "store_performance": (
                store_performance
                .to_dict(orient="records")
            ),
            "top_products": (
                product_performance
                .head(20)
                .to_dict(orient="records")
            ),
            "monthly_demand": (
                monthly_demand
                .to_dict(orient="records")
            ),
            "statistical_analysis": (
                statistical_results
            ),
        }

    @staticmethod
    def _build_prompt(
        user_query: str,
        evidence: dict,
    ) -> str:

        evidence_json = json.dumps(
            evidence,
            indent=2,
            default=str,
        )

        return f"""
You are the Retail Analysis Agent in an
enterprise retail analytics platform.

Analyze the verified analytical evidence
provided below and answer the user's question.

User question:

{user_query}

Verified analytical evidence:

{evidence_json}

Important rules:

1. Do not invent numbers.
2. Do not perform calculations that are not
   supported by the provided evidence.
3. Every important quantitative statement
   should be supported by evidence.
4. Distinguish correlation from causation.
5. Do not claim that a promotion caused a
   demand change unless the evidence supports
   that conclusion.
6. Mention important limitations.
7. Focus on retail business interpretation.
8. Keep the findings concise and actionable.

Return a structured analysis result containing:

- an overall summary
- important findings
- supporting evidence
- limitations
"""

