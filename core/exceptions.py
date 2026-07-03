from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from config.logging import logger
from exceptions.exceptions import (
    BaseApplicationError,
    DatasetNotFoundError,
    FileValidationError,
    FileSizeExceededError,
    InvalidFileTypeError,
    FileParseError,
    DatabaseError,
    AIServiceError
)


class APIException(HTTPException):
    # Base API exception with standardized error handling
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.details = details or {}
        super().__init__(status_code=status_code, detail=message)


def handle_application_error(error: BaseApplicationError) -> APIException:
    # Convert application errors to API exceptions
    logger.error(f"Application error: {error.message}")
    
    if isinstance(error, DatasetNotFoundError):
        return APIException(
            message="Dataset not found",
            status_code=status.HTTP_404_NOT_FOUND,
            details=error.details
        )
    
    if isinstance(error, FileValidationError):
        return APIException(
            message="File validation failed",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=error.details
        )
    
    if isinstance(error, FileSizeExceededError):
        return APIException(
            message="File size exceeds limit",
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            details=error.details
        )
    
    if isinstance(error, InvalidFileTypeError):
        return APIException(
            message="Invalid file type",
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            details=error.details
        )
    
    if isinstance(error, FileParseError):
        return APIException(
            message="Failed to parse file",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=error.details
        )
    
    if isinstance(error, DatabaseError):
        return APIException(
            message="Database operation failed",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=error.details
        )
    
    if isinstance(error, AIServiceError):
        return APIException(
            message="AI service error",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=error.details
        )
    
    # Default error handling
    return APIException(
        message="An unexpected error occurred",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        details=error.details
    )


def handle_generic_error(error: Exception) -> APIException:
    # Handle generic exceptions
    logger.error(f"Unexpected error: {str(error)}")
    return APIException(
        message="An unexpected error occurred",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        details={"error": str(error)}
    )
