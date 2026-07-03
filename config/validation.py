from typing import List, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings
from config.settings import settings
from config.logging import logger


class EnvironmentConfig(BaseSettings):
    # Environment configuration with validation
    
    # Application Settings
    APP_NAME: str = "Finance Analytics Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # File Upload Settings
    MAX_FILE_SIZE_MB: int = 100
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_FILE_TYPES: str = "csv,xlsx,xls"
    
    # DuckDB Settings
    DUCKDB_DATABASE_PATH: str = "./data/finance.duckdb"
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = None
    
    @field_validator('ENVIRONMENT')
    @classmethod
    def environment_must_be_valid(cls, v):
        valid_environments = ['development', 'staging', 'production']
        if v not in valid_environments:
            raise ValueError(f'Environment must be one of {valid_environments}')
        return v
    
    @field_validator('LOG_LEVEL')
    @classmethod
    def log_level_must_be_valid(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of {valid_levels}')
        return v.upper()
    
    @field_validator('PORT')
    @classmethod
    def port_must_be_valid(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v
    
    @field_validator('MAX_FILE_SIZE_MB')
    @classmethod
    def file_size_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Max file size must be positive')
        if v > 1000:  # 1GB limit
            raise ValueError('Max file size cannot exceed 1000MB')
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


def validate_environment() -> List[str]:
    # Validate environment configuration and return list of errors
    errors = []
    
    try:
        config = EnvironmentConfig()
        logger.info("Environment configuration validated successfully")
    except Exception as e:
        errors.append(f"Environment validation failed: {str(e)}")
        logger.error(f"Environment validation error: {e}")
    
    # Check critical environment variables
    openai_key = getattr(settings, 'OPENAI_API_KEY', None)
    environment = getattr(settings, 'environment', 'development')
    
    if not openai_key and environment == "production":
        errors.append("OPENAI_API_KEY is required in production environment")
    
    # Check directories exist
    import os
    upload_dir = getattr(settings, 'upload_dir', './uploads')
    if not os.path.exists(upload_dir):
        errors.append(f"Upload directory does not exist: {upload_dir}")
    
    return errors


def ensure_required_directories():
    # Ensure required directories exist
    import os
    upload_dir = getattr(settings, 'upload_dir', './uploads')
    duckdb_path = getattr(settings, 'duckdb_database_path', './data/finance.duckdb')
    
    directories = [
        upload_dir,
        os.path.dirname(duckdb_path)
    ]
    
    for directory in directories:
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created directory: {directory}")
