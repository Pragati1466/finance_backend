from typing import Dict, List
from sqlalchemy.orm import Session
from repositories.dataset_repository import DatasetRepository
from database.duckdb_manager import DuckDBManager
from config.logging import logger


class SchemaAnalyzer:
    # Extract and analyze database schema information
    
    def __init__(self, session: Session):
        self.session = session
        self.dataset_repo = DatasetRepository(session)
        self.duckdb_manager = DuckDBManager()
    
    def build_schema_summary(self, dataset_id: str) -> str:
        # Build a comprehensive schema summary for AI analysis
        try:
            # Get dataset tables
            tables = self.dataset_repo.get_tables_by_dataset(dataset_id)
            
            if not tables:
                return "No tables found in dataset"
            
            schema_summary = f"Dataset ID: {dataset_id}\n\n"
            schema_summary += f"Total Tables: {len(tables)}\n\n"
            
            # Connect to DuckDB
            self.duckdb_manager.connect()
            
            for table in tables:
                schema_summary += f"Table: {table.table_name}\n"
                schema_summary += f"DuckDB Table: {table.duckdb_table_name}\n"
                schema_summary += f"Rows: {table.row_count}\n"
                schema_summary += f"Columns: {table.column_count}\n"
                
                # Get column information
                columns = self.dataset_repo.get_columns_by_table(str(table.id))
                schema_summary += "Columns:\n"
                
                for col in columns:
                    schema_summary += f"  - {col.column_name} ({col.data_type})"
                    if col.is_nullable == "true":
                        schema_summary += " [nullable]"
                    if col.is_primary_key == "true":
                        schema_summary += " [PRIMARY KEY]"
                    schema_summary += "\n"
                    
                    # Add sample values if available
                    if col.sample_values:
                        try:
                            import ast
                            sample_vals = ast.literal_eval(col.sample_values)
                            if sample_vals:
                                schema_summary += f"    Sample values: {sample_vals[:3]}\n"
                        except:
                            pass
                
                # Get sample rows from DuckDB
                try:
                    sample_query = f"SELECT * FROM {table.duckdb_table_name} LIMIT 3"
                    sample_data = self.duckdb_manager.execute_query(sample_query)
                    
                    if not sample_data.empty:
                        schema_summary += "Sample Data:\n"
                        for idx, row in sample_data.head(3).iterrows():
                            schema_summary += f"  Row {idx + 1}: {dict(row)}\n"
                except Exception as e:
                    logger.warning(f"Could not fetch sample data for {table.table_name}: {e}")
                
                schema_summary += "\n"
            
            # Disconnect from DuckDB
            self.duckdb_manager.disconnect()
            
            return schema_summary
        except Exception as e:
            logger.error(f"Failed to build schema summary: {e}")
            raise
