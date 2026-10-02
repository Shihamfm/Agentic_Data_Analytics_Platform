from analytics_agents.config.settings import settings
from analytics_agents.tools.postgres_executor import (
    PostgreSQLQueryExecutor,
)
from analytics_agents.tools.query_executor import QueryExecutor


def get_query_executor() -> QueryExecutor:

    if settings.environment == "development":
        return PostgreSQLQueryExecutor()

    if settings.environment == "production":
        return PostgreSQLQueryExecutor()

    raise ValueError(
        f"Unsupported environment: "
        f"{settings.environment}"
    )