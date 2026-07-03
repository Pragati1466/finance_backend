from datetime import datetime
from typing import Dict, List
from sqlalchemy.orm import Session
from ai.analyzers.schema_analyzer import SchemaAnalyzer
from ai.llm.openai_client import openai_client
from ai.prompts.schema_analysis import SchemaAnalysisPrompts
from ai.parsers.response_parser import ResponseParser
from ai.generators.kpi_generator import KPIGenerator
from ai.executors.sql_executor import SQLExecutor
from ai.cache.cache_manager import cache_manager
from repositories.dataset_repository import DatasetRepository
from models.ai_models import Relationship, KPI
from schemas.dashboard import DashboardResponse, TableSchema, ColumnSchema, RelationshipSchema, KPISchema
from config.logging import logger


class DashboardService:
    # Service for dashboard operations - coordinates AI components
    
    def __init__(self, session: Session):
        self.session = session
        self.dataset_repo = DatasetRepository(session)
        self.schema_analyzer = SchemaAnalyzer(session)
        self.kpi_generator = KPIGenerator()
        self.sql_executor = SQLExecutor()
    
    def generate_dashboard(self, dataset_id: str) -> DashboardResponse:
        # Generate complete dashboard with schema, relationships, and KPIs
        try:
            logger.info(f"Generating dashboard for dataset {dataset_id}")
            
            # Check if dataset exists
            dataset = self.dataset_repo.get_by_id(dataset_id)
            if not dataset:
                raise Exception("Dataset not found")
            
            # Build schema summary
            schema_summary = self.schema_analyzer.build_schema_summary(dataset_id)
            
            # Analyze schema with AI
            schema_analysis = self._analyze_schema(schema_summary)
            
            # Store relationships
            self._store_relationships(dataset_id, schema_analysis["relationships"])
            
            # Generate KPIs
            kpis = self._generate_and_execute_kpis(
                dataset_id,
                schema_summary,
                schema_analysis["financial_context"]
            )
            
            # Build dashboard response
            dashboard = DashboardResponse(
                dataset_id=dataset_id,
                schema=schema_analysis["tables"],
                relationships=schema_analysis["relationships"],
                financial_context=schema_analysis["financial_context"],
                kpis=kpis,
                execution_status="success",
                generated_at=datetime.now()
            )
            
            logger.info(f"Dashboard generated successfully for dataset {dataset_id}")
            return dashboard
        except Exception as e:
            logger.error(f"Failed to generate dashboard: {e}")
            raise
    
    def _analyze_schema(self, schema_summary: str) -> Dict:
        # Analyze schema using AI
        try:
            # Build prompt
            messages = SchemaAnalysisPrompts.build_schema_analysis_prompt(schema_summary)
            
            # Call AI
            response_text = openai_client.chat_completion(
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )
            
            # Parse response
            parsed = ResponseParser.extract_schema_analysis(response_text)
            
            # Convert to schema objects
            tables = [
                TableSchema(
                    name=table["name"],
                    description=table["description"],
                    columns=[
                        ColumnSchema(
                            name=col["name"],
                            type=col["type"],
                            meaning=col["meaning"],
                            is_primary_key=col["is_primary_key"],
                            is_foreign_key=col["is_foreign_key"],
                            references=col.get("references")
                        )
                        for col in table["columns"]
                    ]
                )
                for table in parsed["tables"]
            ]
            
            relationships = [
                RelationshipSchema(
                    source_table=rel["source_table"],
                    source_column=rel["source_column"],
                    target_table=rel["target_table"],
                    target_column=rel["target_column"],
                    relationship_type=rel["relationship_type"],
                    confidence=rel["confidence"]
                )
                for rel in parsed["relationships"]
            ]
            
            return {
                "tables": tables,
                "relationships": relationships,
                "financial_context": parsed["financial_context"]
            }
        except Exception as e:
            logger.error(f"Failed to analyze schema: {e}")
            raise
    
    def _store_relationships(self, dataset_id: str, relationships: List[RelationshipSchema]):
        # Store relationships in database
        for rel in relationships:
            try:
                self.session.add(Relationship(
                    dataset_id=dataset_id,
                    source_table=rel.source_table,
                    source_column=rel.source_column,
                    target_table=rel.target_table,
                    target_column=rel.target_column,
                    relationship_type=rel.relationship_type,
                    confidence_score=rel.confidence
                ))
                self.session.commit()
            except Exception as e:
                logger.warning(f"Failed to store relationship: {e}")
    
    def _generate_and_execute_kpis(self, dataset_id: str, schema_summary: str, financial_context: str) -> List[KPISchema]:
        # Generate KPIs and execute queries
        try:
            # Generate KPIs
            kpi_definitions = self.kpi_generator.generate_kpis(schema_summary, financial_context)
            
            kpi_schemas = []
            
            for kpi_def in kpi_definitions:
                # Check cache
                cached_result = cache_manager.get(dataset_id, kpi_def["name"])
                
                if cached_result:
                    # Use cached result
                    kpi_schemas.append(KPISchema(
                        id="cached",
                        name=kpi_def["name"],
                        description=kpi_def["description"],
                        category=kpi_def["category"],
                        sql_query=kpi_def["sql_query"],
                        computed_value=cached_result.get("value"),
                        execution_status="success",
                        execution_message=cached_result.get("message"),
                        is_cached=True,
                        computed_at=datetime.now()
                    ))
                    continue
                
                # Execute query
                result = self.sql_executor.execute_query(kpi_def["sql_query"])
                
                # Store KPI in database
                kpi_record = KPI(
                    dataset_id=dataset_id,
                    name=kpi_def["name"],
                    description=kpi_def["description"],
                    category=kpi_def["category"],
                    sql_query=kpi_def["sql_query"],
                    computed_value=result.get("value"),
                    execution_status="success" if result["success"] else "failed",
                    execution_message=result.get("message"),
                    is_cached="false"
                )
                self.session.add(kpi_record)
                self.session.commit()
                
                # Cache result
                if result["success"]:
                    cache_manager.set(dataset_id, kpi_def["name"], result)
                
                kpi_schemas.append(KPISchema(
                    id=str(kpi_record.id),
                    name=kpi_def["name"],
                    description=kpi_def["description"],
                    category=kpi_def["category"],
                    sql_query=kpi_def["sql_query"],
                    computed_value=result.get("value"),
                    execution_status="success" if result["success"] else "failed",
                    execution_message=result.get("message"),
                    is_cached=False,
                    computed_at=kpi_record.created_at
                ))
            
            return kpi_schemas
        except Exception as e:
            logger.error(f"Failed to generate KPIs: {e}")
            raise
