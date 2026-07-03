import uuid
import time
from pathlib import Path
from typing import Dict
import pandas as pd
from sqlalchemy.orm import Session
from config.settings import settings
from config.logging import logger
from constants.constants import (
    DATASET_STATUS_UPLOADING,
    DATASET_STATUS_PARSING,
    DATASET_STATUS_READY,
    DATASET_STATUS_ERROR,
    TABLE_NAME_PATTERN
)
from repositories.dataset_repository import DatasetRepository
from utils.file_parser import FileParser
from database.duckdb_manager import DuckDBManager
from exceptions.exceptions import DatasetNotFoundError, DatabaseError


class DatasetService:
    # Service for dataset business logic
    
    def __init__(self, session: Session):
        self.session = session
        self.dataset_repo = DatasetRepository(session)
        self.file_parser = FileParser()
        self.duckdb_manager = DuckDBManager()
    
    def create_dataset(self, name: str, original_filename: str, file_format: str, file_path: str, file_size: int) -> Dict:
        # Create a new dataset record
        try:
            dataset = self.dataset_repo.create(
                name=name,
                original_filename=original_filename,
                file_path=file_path,
                file_size=file_size,
                file_format=file_format,
                status=DATASET_STATUS_UPLOADING
            )
            logger.info(f"Created dataset {dataset.id}")
            return {"dataset_id": str(dataset.id), "status": dataset.status}
        except Exception as e:
            logger.error(f"Failed to create dataset: {e}")
            raise DatabaseError("create_dataset", str(e))
    
    def process_dataset(self, dataset_id: str) -> Dict:
        # Process uploaded dataset: parse file, store in DuckDB, save metadata
        try:
            # Get dataset
            dataset = self.dataset_repo.get_by_id(dataset_id)
            if not dataset:
                raise DatasetNotFoundError(dataset_id)
            
            # Update status to parsing
            self.dataset_repo.update_status(dataset_id, DATASET_STATUS_PARSING)
            
            # Parse file
            dataframes = self.file_parser.parse_file(dataset.file_path)
            
            # Connect to DuckDB
            self.duckdb_manager.connect()
            
            total_rows = 0
            table_count = 0
            table_counter = 0
            
            # Process each table/sheet
            for table_name, dataframe in dataframes.items():
                # Generate unique DuckDB table name (use timestamp + counter)
                timestamp = int(time.time())
                table_counter += 1
                duckdb_table_name = f"ds_{timestamp}_{table_counter}"
                
                # Create table in DuckDB
                self.duckdb_manager.create_table_from_dataframe(duckdb_table_name, dataframe)
                
                # Create table record
                table_record = self.dataset_repo.create_table(
                    dataset_id=dataset_id,
                    table_name=table_name,
                    original_sheet_name=table_name,
                    row_count=len(dataframe),
                    column_count=len(dataframe.columns),
                    duckdb_table_name=duckdb_table_name
                )
                
                # Extract and store column metadata
                metadata = self.file_parser.extract_metadata(dataframe)
                for column_metadata in metadata["columns"]:
                    self.dataset_repo.create_column(
                        table_id=str(table_record.id),
                        column_name=column_metadata["name"],
                        data_type=column_metadata["data_type"],
                        is_nullable=str(column_metadata["is_nullable"]),
                        is_primary_key="false",
                        sample_values=str(column_metadata["sample_values"]),
                        min_value=str(column_metadata.get("min_value")),
                        max_value=str(column_metadata.get("max_value")),
                        unique_count=column_metadata["unique_count"],
                        null_count=column_metadata["null_count"]
                    )
                
                total_rows += len(dataframe)
                table_count += 1
            
            # Update dataset with totals
            self.dataset_repo.update(
                dataset_id,
                row_count_total=total_rows,
                table_count=table_count,
                status=DATASET_STATUS_READY
            )
            
            # Disconnect from DuckDB
            self.duckdb_manager.disconnect()
            
            logger.info(f"Processed dataset {dataset_id}: {table_count} tables, {total_rows} rows")
            return {
                "dataset_id": dataset_id,
                "status": DATASET_STATUS_READY,
                "table_count": table_count,
                "row_count": total_rows
            }
        except Exception as e:
            logger.error(f"Failed to process dataset {dataset_id}: {e}")
            self.dataset_repo.update_status(dataset_id, DATASET_STATUS_ERROR)
            raise DatabaseError("process_dataset", str(e))
    
    def get_dataset(self, dataset_id: str) -> Dict:
        # Get dataset by ID
        dataset = self.dataset_repo.get_by_id(dataset_id)
        if not dataset:
            raise DatasetNotFoundError(dataset_id)
        return dataset
    
    def get_all_datasets(self, skip: int = 0, limit: int = 100) -> list:
        # Get all datasets with pagination
        return self.dataset_repo.get_all(skip=skip, limit=limit)
