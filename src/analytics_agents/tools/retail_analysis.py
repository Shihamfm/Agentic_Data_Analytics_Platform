import pandas as pd


def calculate_summary_metrics(
    dataframe: pd.DataFrame,
) -> dict:

    if dataframe.empty:
        return {
            "row_count": 0,
            "total_units_sold": 0,
            "total_revenue": 0,
            "average_unit_price": 0,
        }

    total_units = dataframe["units_sold"].sum()

    total_revenue = dataframe["sales_amount"].sum()

    average_unit_price = (
        total_revenue / total_units
        if total_units
        else 0
    )

    return {
        "row_count": len(dataframe),
        "total_units_sold": int(total_units),
        "total_revenue": float(total_revenue),
        "average_unit_price": float(
            average_unit_price
        ),
    }


def calculate_category_performance(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    return (
        dataframe
        .groupby("category", as_index=False)
        .agg(
            units_sold=(
                "units_sold",
                "sum",
            ),
            revenue=(
                "sales_amount",
                "sum",
            ),
        )
        .sort_values(
            "units_sold",
            ascending=False,
        )
    )


def calculate_store_performance(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    return (
        dataframe
        .groupby("store_id", as_index=False)
        .agg(
            units_sold=(
                "units_sold",
                "sum",
            ),
            revenue=(
                "sales_amount",
                "sum",
            ),
        )
        .sort_values(
            "units_sold",
            ascending=False,
        )
    )


def calculate_product_performance(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    return (
        dataframe
        .groupby(
            ["product_id", "category"],
            as_index=False,
        )
        .agg(
            units_sold=(
                "units_sold",
                "sum",
            ),
            revenue=(
                "sales_amount",
                "sum",
            ),
        )
        .sort_values(
            "units_sold",
            ascending=False,
        )
    )

def calculate_monthly_demand(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    data = dataframe.copy()

    data["sales_date"] = pd.to_datetime(
        data["sales_date"]
    )

    monthly = (
        data
        .assign(
            month=data["sales_date"].dt.to_period(
                "M"
            )
        )
        .groupby("month", as_index=False)
        .agg(
            units_sold=(
                "units_sold",
                "sum",
            ),
            revenue=(
                "sales_amount",
                "sum",
            ),
        )
    )

    monthly["month"] = (
        monthly["month"]
        .astype(str)
    )

    monthly["demand_change_pct"] = (
        monthly["units_sold"]
        .pct_change()
        .mul(100)
    )

    return monthly