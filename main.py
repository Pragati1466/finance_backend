from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config.settings import settings
from config.logging import logger, setup_logging
from dependencies.database import init_db
from routers.upload import router as upload_router
from routers.health import router as health_router
from routers.dashboard import router as dashboard_router
from routers.query import router as query_router
from middlewares.error_handler import error_handler
from middlewares.request_logging import request_logging


# Initialize logging
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application lifespan management
    logger.info("Starting application...")
    init_db()
    logger.info("Application started successfully")
    yield
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered Financial Analytics Backend",
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.middleware("http")(request_logging)
app.middleware("http")(error_handler)

# Register routers
app.include_router(upload_router)
app.include_router(health_router)
app.include_router(dashboard_router)
app.include_router(query_router)


@app.get("/")
async def root():
    # Root endpoint
    return {
        "message": "Finance Analytics Backend",
        "version": settings.app_version,
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
