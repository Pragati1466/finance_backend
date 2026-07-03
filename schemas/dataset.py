from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DatasetCreate(BaseModel):
    # Schema for creating a new dataset
    name: str = Field(..., description="Dataset name")
    original_filename: str = Field(..., description="Original filename")
    file_format: str = Field(..., description="File format (csv, xlsx, xls)")


class DatasetResponse(BaseModel):
    # Schema for dataset response
    id: str = Field(..., description="Dataset ID")
    name: str = Field(..., description="Dataset name")
    original_filename: str = Field(..., description="Original filename")
    file_path: str = Field(..., description="File path")
    file_size: int = Field(..., description="File size in bytes")
    file_format: str = Field(..., description="File format")
    status: str = Field(..., description="Dataset status")
    row_count_total: Optional[int] = Field(None, description="Total row count")
    table_count: Optional[int] = Field(None, description="Number of tables")
    upload_date: datetime = Field(..., description="Upload date")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class TableResponse(BaseModel):
    # Schema for table metadata response
    id: str = Field(..., description="Table ID")
    dataset_id: str = Field(..., description="Dataset ID")
    table_name: str = Field(..., description="Table name")
    original_sheet_name: Optional[str] = Field(None, description="Original sheet name for Excel")
    row_count: int = Field(..., description="Number of rows")
    column_count: int = Field(..., description="Number of columns")
    duckdb_table_name: str = Field(..., description="DuckDB table name")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True


class ColumnResponse(BaseModel):
    # Schema for column metadata response
    id: str = Field(..., description="Column ID")
    table_id: str = Field(..., description="Table ID")
    column_name: str = Field(..., description="Column name")
    data_type: str = Field(..., description="Data type")
    is_nullable: bool = Field(..., description="Whether column is nullable")
    is_primary_key: bool = Field(..., description="Whether column is primary key")
    sample_values: Optional[list] = Field(None, description="Sample values")
    min_value: Optional[float] = Field(None, description="Minimum value for numeric columns")
    max_value: Optional[float] = Field(None, description="Maximum value for numeric columns")
    unique_count: Optional[int] = Field(None, description="Number of unique values")
    null_count: Optional[int] = Field(None, description="Number of null values")
    
    class Config:
        from_attributes = True
