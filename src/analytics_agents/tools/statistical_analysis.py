import pandas as pd

from analytics_agents.tools.statistics import (
    calculate_contribution,
    calculate_demand_correlations,
    compare_promotion_demand,
    detect_anomalies,
)


class RetailStatisticalAnalyzer:

    def analyze(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:

        return {
            "category_contribution": (
                calculate_contribution(
                    dataframe,
                    dimension="category",
                    metric="units_sold",
                )
                .to_dict(
                    orient="records"
                )
            ),

            "promotion_comparison": (
                compare_promotion_demand(
                    dataframe
                )
                .to_dict(
                    orient="records"
                )
            ),

            "demand_correlations": (
                calculate_demand_correlations(
                    dataframe
                )
                .to_dict(
                    orient="records"
                )
            ),

            "demand_anomalies": (
                detect_anomalies(
                    dataframe,
                    column="units_sold",
                )
                .query(
                    "is_anomaly == True"
                )
                .to_dict(
                    orient="records"
                )
            ),
        }