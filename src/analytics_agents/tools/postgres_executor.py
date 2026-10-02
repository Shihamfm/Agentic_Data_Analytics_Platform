import pandas as pd
from psycopg import AsyncConnection

from analytics_agents.config.settings import settings
from analytics_agents.tools.query_executor import QueryExecutor


class PostgreSQLQueryExecutor(QueryExecutor):

    def __init__(self):

        if not settings.postgres_host:
            raise ValueError(
                "POSTGRES_HOST is not configured."
            )

        if not settings.postgres_database:
            raise ValueError(
                "POSTGRES_DATABASE is not configured."
            )

        if not settings.postgres_user:
            raise ValueError(
                "POSTGRES_USER is not configured."
            )

        if not settings.postgres_password:
            raise ValueError(
                "POSTGRES_PASSWORD is not configured."
            )

    async def execute(
        self,
        sql: str,
    ) -> pd.DataFrame:

        connection = await AsyncConnection.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            dbname=settings.postgres_database,
            user=settings.postgres_user,
            password=settings.postgres_password,
            sslmode=settings.postgres_sslmode,
        )

        try:

            async with connection.cursor() as cursor:

                await cursor.execute(sql)

                rows = await cursor.fetchall()

                columns = [
                    column.name
                    for column in cursor.description
                ]

                return pd.DataFrame(
                    rows,
                    columns=columns,
                )

        finally:

            await connection.close()