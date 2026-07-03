from datetime import datetime
from typing import Dict, List
from sqlalchemy.orm import Session
from ai.generators.kpi_generator import KPIGenerator
from ai.executors.sql_executor import SQLExecutor
from ai.cache.cache_manager import CacheManager
from models.ai_models import KPI
from schemas.dashboard import KPISchema
from config.logging import logger


class DashboardKPIExecutor:
    # Handles KPI generation and execution for dashboard
    
    def __init__(self, session: Session, cache_manager: CacheManager):
        self.session = session
        self.cache_manager = cache_manager
        self.kpi_generator = KPIGenerator()
        self.sql_executor = SQLExecutor()
    
    def generate_and_execute_kpis(self, dataset_id: str, schema_summary: str, financial_context: str) -> List[KPISchema]:
        # Generate KPIs and execute queries
        try:
            logger.info(f"Generating KPIs for dataset {dataset_id}")
            
            # Generate KPI definitions
            kpi_definitions = self.kpi_generator.generate_kpis(schema_summary, financial_context)
            
            kpi_schemas = []
            
            for kpi_def in kpi_definitions:
                kpi_schema = self._process_single_kpi(dataset_id, kpi_def)
                kpi_schemas.append(kpi_schema)
            
            logger.info(f"Generated {len(kpi_schemas)} KPIs for dataset {dataset_id}")
            return kpi_schemas
        except Exception as e:
            logger.error(f"Failed to generate KPIs: {e}")
            raise
    
    def _process_single_kpi(self, dataset_id: str, kpi_def: Dict) -> KPISchema:
        # Process a single KPI: check cache, execute, store, return schema
        # Check cache first
        cached_result = self.cache_manager.get(dataset_id, kpi_def["name"])
        
        if cached_result:
            return self._create_cached_kpi_schema(kpi_def, cached_result)
        
        # Execute query
        result = self.sql_executor.execute_query(kpi_def["sql_query"])
        
        # Store KPI in database
        kpi_record = self._store_kpi_record(dataset_id, kpi_def, result)
        
        # Cache result if successful
        if result["success"]:
            self.cache_manager.set(dataset_id, kpi_def["name"], result)
        
        return self._create_kpi_schema(kpi_def, result, kpi_record)
    
    def _create_cached_kpi_schema(self, kpi_def: Dict, cached_result: Dict) -> KPISchema:
        # Create KPI schema from cached result
        return KPISchema(
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
        )
    
    def _store_kpi_record(self, dataset_id: str, kpi_def: Dict, result: Dict) -> KPI:
        # Store KPI record in database
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
        return kpi_record
    
    def _create_kpi_schema(self, kpi_def: Dict, result: Dict, kpi_record: KPI) -> KPISchema:
        # Create KPI schema from execution result
        return KPISchema(
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
        )
