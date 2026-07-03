# Dataset Status Constants
DATASET_STATUS_UPLOADING = "uploading"
DATASET_STATUS_PARSING = "parsing"
DATASET_STATUS_READY = "ready"
DATASET_STATUS_ERROR = "error"

# File Type Constants
FILE_TYPE_CSV = "csv"
FILE_TYPE_XLSX = "xlsx"
FILE_TYPE_XLS = "xls"

# Supported File Types
SUPPORTED_FILE_TYPES = [FILE_TYPE_CSV, FILE_TYPE_XLSX, FILE_TYPE_XLS]

# DuckDB Table Naming Pattern
TABLE_NAME_PATTERN = "ds_{dataset_id_short}_{table_name}"

# Error Messages
ERROR_INVALID_FILE_TYPE = "Invalid file type. Supported types: csv, xlsx, xls"
ERROR_FILE_TOO_LARGE = "File size exceeds maximum allowed size"
ERROR_DATASET_NOT_FOUND = "Dataset not found"
ERROR_PARSING_FAILED = "Failed to parse file"
ERROR_DATABASE_ERROR = "Database operation failed"
