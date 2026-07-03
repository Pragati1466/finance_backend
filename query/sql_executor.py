from typing import Dict, Any, List
import pandas as pd
from database.duckdb_manager import DuckDBManager
from config.logging import logger
from exceptions.exceptions import DatabaseError


class QuerySQLExecutor:
    # Execute SQL queries for conversational queries
    
    def __init__(self):
        self.duckdb_manager = DuckDBManager()
    
    def execute_query(self, sql: str) -> Dict[str, Any]:
        # Execute SQL query and return results
        try:
            logger.info("Executing SQL query")
            
            # Connect to DuckDB
            self.duckdb_manager.connect()
            
            # Execute query
            result_df = self.duckdb_manager.execute_query(sql)
            
            # Disconnect
            self.duckdb_manager.disconnect()
            
            # Format result
            if result_df.empty:
                return {
                    "success": True,
                    "row_count": 0,
                    "data": [],
                    "message": "Query executed successfully but returned no results"
                }
            
            # Convert to list of dicts
            data = result_df.to_dict("records")
            
            logger.info(f"Query executed successfully, returned {len(data)} rows")
            return {
                "success": True,
                "row_count": len(data),
                "data": data,
                "message": f"Query executed successfully, returned {len(data)} rows"
            }
        except DatabaseError as e:
            logger.error(f"Database error during query execution: {e}")
            return {
                "success": False,
                "row_count": 0,
                "data": [],
                "message": f"Database error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {e}")
            return {
                "success": False,
                "row_count": 0,
                "data": [],
                "message": f"Query execution failed: {str(e)}"
            }
