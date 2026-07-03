from typing import Dict, Any, Optional
import pandas as pd
from database.duckdb_manager import DuckDBManager
from config.logging import logger
from exceptions.exceptions import DatabaseError


class SQLExecutor:
    # Unified SQL executor for all query operations
    
    def __init__(self, duckdb_manager: Optional[DuckDBManager] = None):
        self.duckdb_manager = duckdb_manager or DuckDBManager()
    
    def execute_query(self, sql: str, return_single_value: bool = False) -> Dict[str, Any]:
        # Execute SQL query and return formatted results
        try:
            logger.info(f"Executing SQL query")
            
            self.duckdb_manager.connect()
            result_df = self.duckdb_manager.execute_query(sql)
            self.duckdb_manager.disconnect()
            
            if result_df.empty:
                return self._format_empty_result()
            
            if return_single_value and len(result_df) == 1 and len(result_df.columns) == 1:
                return self._format_single_value_result(result_df)
            
            return self._format_table_result(result_df)
            
        except DatabaseError as e:
            logger.error(f"Database error during query execution: {e}")
            return self._format_error_result(f"Database error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {e}")
            return self._format_error_result(f"Query execution failed: {str(e)}")
    
    def _format_empty_result(self) -> Dict[str, Any]:
        # Format empty result set
        return {
            "success": True,
            "row_count": 0,
            "data": [],
            "value": None,
            "message": "Query executed successfully but returned no results"
        }
    
    def _format_single_value_result(self, result_df: pd.DataFrame) -> Dict[str, Any]:
        # Format single value result (for KPIs)
        value = result_df.iloc[0, 0]
        return {
            "success": True,
            "row_count": 1,
            "data": [value],
            "value": float(value) if pd.notna(value) else None,
            "message": "Query executed successfully"
        }
    
    def _format_table_result(self, result_df: pd.DataFrame) -> Dict[str, Any]:
        # Format table result (for conversational queries)
        data = result_df.to_dict("records")
        logger.info(f"Query executed successfully, returned {len(data)} rows")
        return {
            "success": True,
            "row_count": len(data),
            "data": data,
            "value": data,
            "message": f"Query executed successfully, returned {len(data)} rows"
        }
    
    def _format_error_result(self, message: str) -> Dict[str, Any]:
        # Format error result
        return {
            "success": False,
            "row_count": 0,
            "data": [],
            "value": None,
            "message": message
        }
