from typing import Dict, Any
from sqlalchemy.orm import Session
from ai.analyzers.schema_analyzer import SchemaAnalyzer
from repositories.dataset_repository import DatasetRepository
from query.llm_client import QueryLLMClient
from query.prompt_builder import PromptBuilder
from query.sql_validator import SQLValidator
from query.sql_executor import QuerySQLExecutor
from query.response_formatter import ResponseFormatter
from config.logging import logger
from exceptions.exceptions import DatasetNotFoundError


class QueryService:
    # Service for conversational query processing
    
    def __init__(self, session: Session):
        self.session = session
        self.dataset_repo = DatasetRepository(session)
        self.schema_analyzer = SchemaAnalyzer(session)
        self.llm_client = QueryLLMClient()
        self.prompt_builder = PromptBuilder()
        self.sql_validator = SQLValidator()
        self.sql_executor = QuerySQLExecutor()
        self.response_formatter = ResponseFormatter()
    
    def process_query(self, dataset_id: str, question: str) -> Dict[str, Any]:
        # Process conversational query end-to-end
        try:
            logger.info(f"Processing query for dataset {dataset_id}: {question}")
            
            # Validate dataset exists
            dataset = self.dataset_repo.get_by_id(dataset_id)
            if not dataset:
                raise DatasetNotFoundError(dataset_id)
            
            # Get schema summary
            schema_summary = self.schema_analyzer.build_schema_summary(dataset_id)
            
            # Get relationships
            tables = self.dataset_repo.get_tables_by_dataset(dataset_id)
            relationships = self._extract_relationships(tables)
            
            # Get KPI context
            kpi_context = self._extract_kpi_context(dataset_id)
            
            # Build prompt
            prompt = self.prompt_builder.build_query_prompt(
                question,
                schema_summary,
                relationships,
                kpi_context
            )
            
            # Generate SQL
            generated_sql = self.llm_client.generate_sql(prompt)
            
            # Sanitize SQL
            generated_sql = self.sql_validator.sanitize_query(generated_sql)
            
            # Validate SQL
            validation_passed, validation_message = self.sql_validator.validate_query(generated_sql)
            
            # Execute query if validation passed
            query_result = {"success": False, "row_count": 0, "data": [], "message": ""}
            if validation_passed:
                query_result = self.sql_executor.execute_query(generated_sql)
            else:
                query_result["message"] = validation_message
            
            # Format response
            response = self.response_formatter.format_query_response(
                question,
                generated_sql,
                query_result,
                validation_passed,
                validation_message
            )
            
            logger.info("Query processed successfully")
            return response
        except DatasetNotFoundError as e:
            logger.error(f"Dataset not found: {e}")
            return self.response_formatter.format_error_response(
                question,
                "Dataset not found"
            )
        except Exception as e:
            logger.error(f"Failed to process query: {e}")
            return self.response_formatter.format_error_response(
                question,
                "An error occurred while processing your query"
            )
    
    def _extract_relationships(self, tables) -> list:
        # Extract relationships from tables
        # In a real implementation, this would come from the AI-generated relationships
        return []
    
    def _extract_kpi_context(self, dataset_id: str) -> str:
        # Extract KPI context for the dataset
        # In a real implementation, this would fetch stored KPI information
        return "Financial data with revenue, expenses, and profit metrics available."
