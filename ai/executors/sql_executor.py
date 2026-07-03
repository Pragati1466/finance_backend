from typing import Dict, Any
import pandas as pd
from database.duckdb_manager import DuckDBManager
from config.logging import logger
from exceptions.exceptions import DatabaseError


class SQLExecutor:
    # Execute SQL queries and return results
    
    def __init__(self):
        self.duckdb_manager = DuckDBManager()
    
    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        # Execute a SQL query and return results
        try:
            logger.info(f"Executing SQL query")
            
            # Connect to DuckDB
            self.duckdb_manager.connect()
            
            # Execute query
            result_df = self.duckdb_manager.execute_query(sql_query)
            
            # Disconnect
            self.duckdb_manager.disconnect()
            
            # Convert result to dict
            if result_df.empty:
                return {
                    "value": None,
                    "row_count": 0,
                    "success": True,
                    "message": "Query returned no results"
                }
            
            # For single value results (most KPIs)
            if len(result_df) == 1 and len(result_df.columns) == 1:
                value = result_df.iloc[0, 0]
                return {
                    "value": float(value) if pd.notna(value) else None,
                    "row_count": 1,
                    "success": True,
                    "message": "Query executed successfully"
                }
            
            # For multi-row/column results
            return {
                    "value": result_df.to_dict("records"),
                    "row_count": len(result_df),
                    "success": True,
                    "message": f"Query returned {len(result_df)} rows"
                }
        except Exception as e:
            logger.error(f"Failed to execute SQL query: {e}")
            return {
                "value": None,
                "row_count": 0,
                "success": False,
                "message": f"Query execution failed: {str(e)}"
            }
