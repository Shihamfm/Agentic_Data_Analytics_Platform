import pandas as pd


def calculate_growth(
    current_value: float,
    previous_value: float,
) -> float | None:

    if previous_value == 0:
        return None

    return (
        (current_value - previous_value)
        / previous_value
    ) * 100

def calculate_contribution(
    dataframe: pd.DataFrame,
    dimension: str,
    metric: str,
) -> pd.DataFrame:

    grouped = (
        dataframe
        .groupby(dimension, as_index=False)[metric]
        .sum()
    )

    total = grouped[metric].sum()

    if total == 0:
        grouped["contribution_pct"] = 0.0
    else:
        grouped["contribution_pct"] = (
            grouped[metric] / total * 100
        )

    return grouped.sort_values(
        metric,
        ascending=False,
    )

def compare_promotion_demand(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    result = (
        dataframe
        .groupby(
            "promotion_flag",
            as_index=False,
        )
        .agg(
            total_units_sold=(
                "units_sold",
                "sum",
            ),
            average_units_sold=(
                "units_sold",
                "mean",
            ),
            total_revenue=(
                "sales_amount",
                "sum",
            ),
            observations=(
                "units_sold",
                "count",
            ),
        )
    )

    return result

def calculate_demand_correlations(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    numeric_columns = [
        "units_sold",
        "unit_price",
        "sales_amount",
        "inventory_units",
    ]

    available_columns = [
        column
        for column in numeric_columns
        if column in dataframe.columns
    ]

    correlation_matrix = (
        dataframe[available_columns]
        .corr()
    )

    demand_correlation = (
        correlation_matrix["units_sold"]
        .drop("units_sold")
        .sort_values(
            key=lambda values: values.abs(),
            ascending=False,
        )
    )

    return (
        demand_correlation
        .rename("correlation")
        .reset_index()
        .rename(
            columns={
                "index": "feature"
            }
        )
    )

def detect_anomalies(
    dataframe: pd.DataFrame,
    column: str,
    threshold: float = 3.0,
) -> pd.DataFrame:

    result = dataframe.copy()

    mean = result[column].mean()

    std = result[column].std()

    if std == 0 or pd.isna(std):
        result["z_score"] = 0.0
        result["is_anomaly"] = False

        return result

    result["z_score"] = (
        (result[column] - mean) / std
    )

    result["is_anomaly"] = (
        result["z_score"].abs()
        >= threshold
    )

    return result