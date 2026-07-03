from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config.settings import settings
from config.logging import logger, setup_logging
from config.validation import ensure_required_directories
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
    
    # Ensure required directories exist
    ensure_required_directories()
    
    # Initialize database
    init_db()
    
    logger.info("Application started successfully")
    yield
    logger.info("Shutting down application...")


# Create FastAPI application with comprehensive API documentation
app = FastAPI(
    title="Finance Analytics Backend",
    version="1.0.0",
    description="""
    AI-powered Financial Analytics Backend for processing and analyzing financial data.
    
    ## Features
    - **File Upload**: Upload CSV and Excel files for analysis
    - **AI-Powered Analysis**: Automatic schema analysis and KPI generation
    - **Conversational Queries**: Natural language to SQL query generation
    - **Dashboard**: Comprehensive financial metrics and insights
    
    ## Authentication
    Currently in development. API will require authentication in production.
    
    ## Rate Limiting
    Rate limiting will be implemented in production.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    contact={
        "name": "Finance Analytics Team",
        "email": "support@finance-analytics.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Add CORS middleware with production-ready configuration
allowed_origins = settings.cors_origins.split(",") if settings.cors_origins else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    # Add security headers to all responses
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; img-src 'self' data:"
    return response

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
