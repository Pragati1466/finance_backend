from datetime import datetime
from typing import Dict, List
from sqlalchemy.orm import Session
from ai.analyzers.schema_analyzer import SchemaAnalyzer
from ai.generators.kpi_generator import KPIGenerator
from ai.executors.sql_executor import SQLExecutor
from ai.cache.cache_manager import cache_manager
from repositories.dataset_repository import DatasetRepository
from models.ai_models import Relationship, KPI
from schemas.dashboard import DashboardResponse, TableSchema, ColumnSchema, RelationshipSchema, KPISchema
from config.logging import logger
from services.dashboard_schema_analyzer import DashboardSchemaAnalyzer
from services.dashboard_kpi_executor import DashboardKPIExecutor


class DashboardService:
    # Service for dashboard operations - coordinates AI components
    
    def __init__(self, session: Session):
        self.session = session
        self.dataset_repo = DatasetRepository(session)
        self.schema_analyzer = SchemaAnalyzer(session)
        self.dashboard_schema_analyzer = DashboardSchemaAnalyzer()
        self.kpi_executor = DashboardKPIExecutor(session, cache_manager)
    
    def generate_dashboard(self, dataset_id: str) -> DashboardResponse:
        # Generate complete dashboard with schema, relationships, and KPIs
        try:
            logger.info(f"Generating dashboard for dataset {dataset_id}")
            
            # Validate dataset exists
            self._validate_dataset(dataset_id)
            
            # Build schema summary
            schema_summary = self.schema_analyzer.build_schema_summary(dataset_id)
            
            # Analyze schema with AI
            schema_analysis = self.dashboard_schema_analyzer.analyze_schema(schema_summary)
            
            # Store relationships
            self._store_relationships(dataset_id, schema_analysis["relationships"])
            
            # Generate and execute KPIs
            kpis = self.kpi_executor.generate_and_execute_kpis(
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
    
    def _validate_dataset(self, dataset_id: str):
        # Validate that dataset exists
        dataset = self.dataset_repo.get_by_id(dataset_id)
        if not dataset:
            raise ValueError(f"Dataset not found: {dataset_id}")
    
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
