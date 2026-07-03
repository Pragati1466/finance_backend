import duckdb
import pandas as pd
from pathlib import Path
from config.settings import settings
from config.logging import logger
from exceptions.exceptions import DatabaseError


class DuckDBManager:
    # Manages DuckDB database connections and operations
    
    def __init__(self, database_path: str = None):
        self.database_path = database_path or settings.duckdb_database_path
        self.connection = None
        self._ensure_database_directory()
    
    def _ensure_database_directory(self):
        # Create database directory if it doesn't exist
        db_path = Path(self.database_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def connect(self):
        # Establish connection to DuckDB database
        try:
            self.connection = duckdb.connect(self.database_path)
            logger.info(f"Connected to DuckDB database at {self.database_path}")
            return self.connection
        except Exception as e:
            logger.error(f"Failed to connect to DuckDB: {e}")
            raise DatabaseError("connect", str(e))
    
    def disconnect(self):
        # Close database connection
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Disconnected from DuckDB database")
    
    def create_table_from_dataframe(self, table_name: str, df: pd.DataFrame):
        # Create a DuckDB table from a pandas DataFrame
        try:
            if not self.connection:
                self.connect()
            
            # Use unique temp name to avoid conflicts
            temp_name = f"temp_df_{table_name}"
            
            # Register DataFrame and create table
            self.connection.register(temp_name, df)
            self.connection.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM {temp_name}")
            self.connection.execute(f"DROP VIEW {temp_name}")
            
            logger.info(f"Created table {table_name} with {len(df)} rows")
            return True
        except Exception as e:
            logger.error(f"Failed to create table {table_name}: {e}")
            raise DatabaseError(f"create_table {table_name}", str(e))
    
    def execute_query(self, query: str):
        # Execute a SQL query and return results
        try:
            if not self.connection:
                self.connect()
            
            result = self.connection.execute(query).fetchdf()
            logger.info(f"Executed query successfully, returned {len(result)} rows")
            return result
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            raise DatabaseError("execute_query", str(e))
    
    def table_exists(self, table_name: str) -> bool:
        # Check if a table exists in the database
        try:
            if not self.connection:
                self.connect()
            
            query = f"SELECT table_name FROM information_schema.tables WHERE table_name = '{table_name}'"
            result = self.connection.execute(query).fetchall()
            return len(result) > 0
        except Exception as e:
            logger.error(f"Failed to check table existence: {e}")
            return False
    
    def drop_table(self, table_name: str):
        # Drop a table from the database
        try:
            if not self.connection:
                self.connect()
            
            self.connection.execute(f"DROP TABLE IF EXISTS {table_name}")
            logger.info(f"Dropped table {table_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to drop table {table_name}: {e}")
            raise DatabaseError(f"drop_table {table_name}", str(e))
    
    def get_table_info(self, table_name: str) -> dict:
        # Get information about a table (columns, types, row count)
        try:
            if not self.connection:
                self.connect()
            
            # Get column information
            columns_query = f"DESCRIBE {table_name}"
            columns = self.connection.execute(columns_query).fetchdf()
            
            # Get row count
            count_query = f"SELECT COUNT(*) as row_count FROM {table_name}"
            row_count = self.connection.execute(count_query).fetchone()[0]
            
            return {
                "table_name": table_name,
                "columns": columns.to_dict("records"),
                "row_count": row_count
            }
        except Exception as e:
            logger.error(f"Failed to get table info for {table_name}: {e}")
            raise DatabaseError(f"get_table_info {table_name}", str(e))


# Global DuckDB manager instance
duckdb_manager = DuckDBManager()
