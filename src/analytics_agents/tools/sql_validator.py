import re

from analytics_agents.data.catalog import RETAIL_CATALOG
from analytics_agents.models.results import (
    SQLValidationResult,
)


FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "MERGE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "GRANT",
    "REVOKE",
}


class SQLValidator:

    def validate(
        self,
        sql: str,
    ) -> SQLValidationResult:

        issues: list[str] = []

        normalized_sql = sql.strip()

        if not normalized_sql:
            issues.append(
                "SQL query is empty."
            )

            return SQLValidationResult(
                approved=False,
                sql=sql,
                issues=issues,
            )

        self._check_multiple_statements(
            normalized_sql,
            issues,
        )

        self._check_read_only(
            normalized_sql,
            issues,
        )

        self._check_select(
            normalized_sql,
            issues,
        )

        self._check_tables(
            normalized_sql,
            issues,
        )

        approved = len(issues) == 0

        return SQLValidationResult(
            approved=approved,
            sql=sql,
            issues=issues,
        )

    @staticmethod
    def _check_multiple_statements(
        sql: str,
        issues: list[str],
    ) -> None:

        statements = [
            statement.strip()
            for statement in sql.split(";")
            if statement.strip()
        ]

        if len(statements) > 1:

            issues.append(
                "Multiple SQL statements are not allowed."
            )
    
    @staticmethod
    def _check_read_only(
        sql: str,
        issues: list[str],
    ) -> None:

        upper_sql = sql.upper()

        for keyword in FORBIDDEN_KEYWORDS:

            pattern = rf"\b{keyword}\b"

            if re.search(pattern, upper_sql):

                issues.append(
                    f"Forbidden SQL operation detected: "
                    f"{keyword}"
                )

    @staticmethod
    def _check_select(
        sql: str,
        issues: list[str],
    ) -> None:

        upper_sql = sql.upper().strip()

        if not upper_sql.startswith("SELECT"):

            issues.append(
                "Only SELECT queries are allowed."
            )
    
    @staticmethod
    def _check_tables(
        sql: str,
        issues: list[str],
    ) -> None:

        known_tables = {
            table.name.lower()
            for table in RETAIL_CATALOG.tables
        }

        referenced_tables = re.findall(
            r"\b(?:FROM|JOIN)\s+([A-Za-z_][\w.]*)",
            sql,
            flags=re.IGNORECASE,
        )

        for table in referenced_tables:

            table_name = table.lower()

            if table_name not in known_tables:

                issues.append(
                    f"Unknown table referenced: {table}"
                )