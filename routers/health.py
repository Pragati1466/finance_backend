from fastapi import APIRouter
from database.duckdb_manager import duckdb_manager
from config.settings import settings
from config.logging import logger


router = APIRouter(prefix="/api/v1/health", tags=["health"])


@router.get(
    "/",
    summary="Health Check",
    description="Check the health status of the application and its dependencies",
    responses={
        200: {
            "description": "Application is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "app_name": "Finance Analytics Backend",
                        "app_version": "1.0.0",
                        "environment": "development",
                        "services": {
                            "duckdb": "healthy"
                        }
                    }
                }
            }
        },
        503: {
            "description": "Application or dependencies are unhealthy"
        }
    }
)
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


@router.get(
    "/version",
    summary="Version Information",
    description="Get the current version of the application",
    responses={
        200: {
            "description": "Version information retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "version": "1.0.0",
                        "app_name": "Finance Analytics Backend",
                        "environment": "development",
                        "build_date": "2024-01-01T00:00:00Z"
                    }
                }
            }
        }
    }
)
async def version():
    # Version information endpoint
    return {
        "version": settings.app_version,
        "app_name": settings.app_name,
        "environment": settings.environment,
        "build_date": "2026-07-03T19:14:00Z"  # Build date: July 3, 2026 at 7:14 PM
    }
