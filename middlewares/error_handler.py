from fastapi import Request, status
from fastapi.responses import JSONResponse
from config.logging import logger
from exceptions.exceptions import (
    BaseApplicationError,
    FileValidationError,
    DatasetNotFoundError,
    FileParseError,
    DatabaseError
)


async def error_handler(request: Request, call_next):
    # Global exception handler for all requests
    try:
        response = await call_next(request)
        return response
    except BaseApplicationError as e:
        # Handle application-specific errors
        logger.error(f"Application error: {e.message}", extra={
            "error_type": type(e).__name__,
            "path": request.url.path,
            "method": request.method
        })
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": e.message,
                "details": e.details,
                "type": type(e).__name__,
                "path": request.url.path
            }
        )
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error: {str(e)}", extra={
            "error_type": "InternalServerError",
            "path": request.url.path,
            "method": request.method
        })
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "Internal server error",
                "type": "InternalServerError",
                "path": request.url.path,
                "details": str(e) if logger.level >= 20 else "An unexpected error occurred"
            }
        )
