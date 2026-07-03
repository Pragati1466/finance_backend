from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Application Settings
    app_name: str = Field(default="Finance Analytics Backend", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment name")

    # Server Settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")

    # File Upload Settings
    max_file_size_mb: int = Field(default=100, description="Maximum file size in MB")
    upload_dir: str = Field(default="./uploads", description="Upload directory")
    allowed_file_types: str = Field(default="csv,xlsx,xls", description="Allowed file types")

    # DuckDB Settings
    duckdb_database_path: str = Field(default="./data/finance.duckdb", description="DuckDB database path")

    # Logging Settings
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="json", description="Log format")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
