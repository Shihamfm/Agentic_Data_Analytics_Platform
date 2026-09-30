from analytics_agents.models.semantic import (
    SemanticCatalog,
    SemanticDimension,
    SemanticMetric,
    SemanticTable,
)


RETAIL_CATALOG = SemanticCatalog(

    tables=[
        SemanticTable(
            name="retail_sales",
            description=(
                "Historical retail sales transactions "
                "at product and store level."
            ),
            columns=[
                "sales_date",
                "product_id",
                "store_id",
                "category",
                "units_sold",
                "unit_price",
                "sales_amount",
                "promotion_flag",
                "inventory_units",
            ],
        )
    ],

    metrics=[
        SemanticMetric(
            name="demand",
            expression="SUM(units_sold)",
            description=(
                "Total units sold, used as the "
                "observed demand measure."
            ),
        ),

        SemanticMetric(
            name="revenue",
            expression="SUM(sales_amount)",
            description=(
                "Total revenue generated from sales."
            ),
        ),

        SemanticMetric(
            name="average_selling_price",
            expression=(
                "SUM(sales_amount) / "
                "NULLIF(SUM(units_sold), 0)"
            ),
            description=(
                "Average selling price per unit."
            ),
        ),

        SemanticMetric(
            name="average_daily_demand",
            expression=(
                "AVG(units_sold)"
            ),
            description=(
                "Average units sold per observation."
            ),
        ),
    ],

    dimensions=[
        SemanticDimension(
            name="product",
            column="product_id",
            description="Unique product identifier.",
        ),

        SemanticDimension(
            name="store",
            column="store_id",
            description="Unique store identifier.",
        ),

        SemanticDimension(
            name="category",
            column="category",
            description="Retail product category.",
        ),

        SemanticDimension(
            name="date",
            column="sales_date",
            description="Date of the sales observation.",
            data_type="date",
        ),

        SemanticDimension(
            name="promotion",
            column="promotion_flag",
            description=(
                "Indicates whether the product was "
                "under promotion."
            ),
            data_type="boolean",
        ),
    ],
)

def get_metric(name: str) -> SemanticMetric:

    for metric in RETAIL_CATALOG.metrics:

        if metric.name.lower() == name.lower():
            return metric

    raise KeyError(
        f"Unknown metric: {name}"
    )


def get_dimension(name: str) -> SemanticDimension:

    for dimension in RETAIL_CATALOG.dimensions:

        if dimension.name.lower() == name.lower():
            return dimension

    raise KeyError(
        f"Unknown dimension: {name}"
    )


def get_table(name: str) -> SemanticTable:

    for table in RETAIL_CATALOG.tables:

        if table.name.lower() == name.lower():
            return table

    raise KeyError(
        f"Unknown table: {name}"
    )