from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ColumnSchema(BaseModel):
    # Schema for column information
    name: str = Field(..., description="Column name")
    type: str = Field(..., description="Data type")
    meaning: str = Field(..., description="Column meaning")
    is_primary_key: bool = Field(..., description="Whether column is primary key")
    is_foreign_key: bool = Field(..., description="Whether column is foreign key")
    references: Optional[str] = Field(None, description="Referenced table.column if foreign key")


class TableSchema(BaseModel):
    # Schema for table information
    name: str = Field(..., description="Table name")
    description: str = Field(..., description="Table description")
    columns: List[ColumnSchema] = Field(..., description="Column information")


class RelationshipSchema(BaseModel):
    # Schema for relationship information
    source_table: str = Field(..., description="Source table name")
    source_column: str = Field(..., description="Source column name")
    target_table: str = Field(..., description="Target table name")
    target_column: str = Field(..., description="Target column name")
    relationship_type: str = Field(..., description="Relationship type")
    confidence: float = Field(..., description="Confidence score")


class KPISchema(BaseModel):
    # Schema for KPI information
    id: str = Field(..., description="KPI ID")
    name: str = Field(..., description="KPI name")
    description: str = Field(..., description="KPI description")
    category: str = Field(..., description="KPI category")
    sql_query: str = Field(..., description="SQL query to calculate KPI")
    computed_value: Optional[float] = Field(None, description="Computed KPI value")
    execution_status: str = Field(..., description="Execution status")
    execution_message: Optional[str] = Field(None, description="Execution message")
    is_cached: bool = Field(..., description="Whether result is cached")
    computed_at: Optional[datetime] = Field(None, description="Computation timestamp")


class DashboardResponse(BaseModel):
    # Schema for dashboard response
    dataset_id: str = Field(..., description="Dataset ID")
    schema: List[TableSchema] = Field(..., description="Table schemas")
    relationships: List[RelationshipSchema] = Field(..., description="Table relationships")
    financial_context: str = Field(..., description="Financial context")
    kpis: List[KPISchema] = Field(..., description="Generated KPIs")
    execution_status: str = Field(..., description="Overall execution status")
    generated_at: datetime = Field(..., description="Generation timestamp")
