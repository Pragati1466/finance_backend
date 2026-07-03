from constants.constants import (
    ERROR_INVALID_FILE_TYPE,
    ERROR_FILE_TOO_LARGE,
    ERROR_DATASET_NOT_FOUND,
    ERROR_PARSING_FAILED,
    ERROR_DATABASE_ERROR
)


class BaseApplicationError(Exception):
    # Base exception for all application-specific errors
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class FileValidationError(BaseApplicationError):
    # Raised when file validation fails
    pass


class FileSizeExceededError(FileValidationError):
    # Raised when file size exceeds limit
    def __init__(self, max_size_mb: int):
        super().__init__(ERROR_FILE_TOO_LARGE, {"max_size_mb": max_size_mb})


class InvalidFileTypeError(FileValidationError):
    # Raised when file type is not supported
    def __init__(self, file_type: str):
        super().__init__(ERROR_INVALID_FILE_TYPE, {"file_type": file_type})


class DatasetNotFoundError(BaseApplicationError):
    # Raised when dataset is not found
    def __init__(self, dataset_id: str):
        super().__init__(ERROR_DATASET_NOT_FOUND, {"dataset_id": dataset_id})


class FileParseError(BaseApplicationError):
    # Raised when file parsing fails
    def __init__(self, original_error: str = None):
        message = ERROR_PARSING_FAILED
        if original_error:
            message = f"{ERROR_PARSING_FAILED}: {original_error}"
        super().__init__(message, {"original_error": original_error})


class DatabaseError(BaseApplicationError):
    # Raised when database operation fails
    def __init__(self, operation: str, original_error: str = None):
        message = f"{ERROR_DATABASE_ERROR}: {operation}"
        if original_error:
            message = f"{message} - {original_error}"
        super().__init__(message, {"operation": operation, "original_error": original_error})


class AIServiceError(BaseApplicationError):
    # Raised when AI service operation fails
    def __init__(self, message: str):
        super().__init__(message, {})
