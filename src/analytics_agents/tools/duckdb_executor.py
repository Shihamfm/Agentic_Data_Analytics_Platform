import duckdb
import pandas as pd

from analytics_agents.tools.query_executor import QueryExecutor


class DuckDBQueryExecutor(QueryExecutor):

    def __init__(
        self,
        dataframe: pd.DataFrame,
        table_name: str = "retail_sales",
    ):
        self.dataframe = dataframe
        self.table_name = table_name

    async def execute(
        self,
        sql: str,
    ) -> pd.DataFrame:

        connection = duckdb.connect(database=":memory:")

        try:

            connection.register(
                self.table_name,
                self.dataframe,
            )

            result = connection.execute(sql).fetchdf()

            return result

        finally:

            connection.close()