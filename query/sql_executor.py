from typing import Dict, Any
from database.sql_executor import SQLExecutor as BaseSQLExecutor
from config.logging import logger


class QuerySQLExecutor(BaseSQLExecutor):
    # SQL executor specialized for conversational queries (table results)
    
    def execute_query(self, sql: str) -> Dict[str, Any]:
        # Execute query and return table format for conversational queries
        return super().execute_query(sql, return_single_value=False)
