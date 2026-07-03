from fastapi import APIRouter
from database.duckdb_manager import duckdb_manager
from config.settings import settings
from config.logging import logger


router = APIRouter(prefix="/api/v1/health", tags=["health"])


@router.get("/")
async def health_check():
    # Health check endpoint for monitoring
    
    health_status = {
        "status": "healthy",
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "environment": settings.environment,
        "services": {
            "duckdb": "unknown"
        }
    }
    
    # Check DuckDB connection
    try:
        duckdb_manager.connect()
        health_status["services"]["duckdb"] = "healthy"
        duckdb_manager.disconnect()
    except Exception as e:
        logger.error(f"DuckDB health check failed: {e}")
        health_status["services"]["duckdb"] = "unhealthy"
        health_status["status"] = "degraded"
    
    return health_status
