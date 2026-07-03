from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict


class QueryRequest(BaseModel):
    # Schema for query request
    question: str = Field(..., description="Natural language question about the data")
    dataset_id: str = Field(..., description="Dataset ID to query")


class QueryResult(BaseModel):
    # Schema for query execution result
    success: bool = Field(..., description="Whether query executed successfully")
    row_count: int = Field(..., description="Number of rows returned")
    data: List[Dict[str, Any]] = Field(..., description="Query result data")
    message: str = Field(..., description="Execution message")


class ValidationInfo(BaseModel):
    # Schema for validation information
    passed: bool = Field(..., description="Whether validation passed")
    message: str = Field(..., description="Validation message")


class QueryResponse(BaseModel):
    # Schema for query response
    question: str = Field(..., description="Original question")
    generated_sql: Optional[str] = Field(None, description="Generated SQL query")
    query_result: QueryResult = Field(..., description="Query execution result")
    validation: ValidationInfo = Field(..., description="Validation information")
    explanation: str = Field(..., description="Natural language explanation")
