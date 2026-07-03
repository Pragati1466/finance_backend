from typing import Any, Dict, Optional
from fastapi import status
from pydantic import BaseModel


class APIResponse(BaseModel):
    # Standardized API response wrapper
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[list] = None
    status_code: int = status.HTTP_200_OK


class ErrorResponse(BaseModel):
    # Standardized error response
    success: bool = False
    message: str
    errors: Optional[list] = None
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


def success_response(data: Any = None, message: str = "Operation successful") -> Dict[str, Any]:
    # Create standardized success response
    return {
        "success": True,
        "message": message,
        "data": data,
        "errors": None,
        "status_code": status.HTTP_200_OK
    }


def error_response(message: str, errors: Optional[list] = None, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR) -> Dict[str, Any]:
    # Create standardized error response
    return {
        "success": False,
        "message": message,
        "data": None,
        "errors": errors,
        "status_code": status_code
    }
