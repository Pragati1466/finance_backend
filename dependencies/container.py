from typing import TypeVar, Type, Callable, Dict, Any
from functools import lru_cache
from sqlalchemy.orm import Session
from database.duckdb_manager import DuckDBManager
from database.sql_executor import SQLExecutor
from repositories.dataset_repository import DatasetRepository
from services.dataset_service import DatasetService
from services.dashboard_service import DashboardService
from query.query_service import QueryService
from config.logging import logger


T = TypeVar('T')


class DIContainer:
    # Dependency injection container for managing service dependencies
    
    def __init__(self):
        self._factories: Dict[Type, Callable[..., Any]] = {}
        self._singletons: Dict[Type, Any] = {}
        self._register_defaults()
    
    def _register_defaults(self):
        # Register default factory methods for common dependencies
        self.register_factory(DuckDBManager, lambda: DuckDBManager())
        self.register_factory(SQLExecutor, lambda: SQLExecutor())
    
    def register_factory(self, interface: Type[T], factory: Callable[..., T]):
        # Register a factory method for creating instances
        self._factories[interface] = factory
        logger.debug(f"Registered factory for {interface.__name__}")
    
    def register_singleton(self, interface: Type[T], instance: T):
        # Register a singleton instance
        self._singletons[interface] = instance
        logger.debug(f"Registered singleton for {interface.__name__}")
    
    def resolve(self, interface: Type[T]) -> T:
        # Resolve a dependency by type
        # Check singletons first
        if interface in self._singletons:
            return self._singletons[interface]
        
        # Check factories
        if interface in self._factories:
            return self._factories[interface]()
        
        # Try to instantiate directly
        try:
            return interface()
        except Exception as e:
            logger.error(f"Failed to resolve dependency {interface.__name__}: {e}")
            raise ValueError(f"Cannot resolve dependency: {interface.__name__}")
    
    def get_dataset_service(self, session: Session) -> DatasetService:
        # Get dataset service with session dependency
        return DatasetService(session)
    
    def get_dashboard_service(self, session: Session) -> DashboardService:
        # Get dashboard service with session dependency
        return DashboardService(session)
    
    def get_query_service(self, session: Session) -> QueryService:
        # Get query service with session dependency
        return QueryService(session)


# Global container instance
container = DIContainer()
