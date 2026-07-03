from typing import Dict, Any
from database.sql_executor import SQLExecutor as BaseSQLExecutor
from config.logging import logger


class SQLExecutor(BaseSQLExecutor):
    # SQL executor specialized for AI-generated queries (single value results)
    
    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        # Execute query and return single value format for KPIs
        return super().execute_query(sql_query, return_single_value=True)
