from abc import ABC, abstractmethod

import pandas as pd


class QueryExecutor(ABC):

    @abstractmethod
    async def execute(
        self,
        sql: str,
    ) -> pd.DataFrame:
        """Execute read-only SQL and return a DataFrame."""
    
