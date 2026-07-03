from typing import Optional, Dict, Any
from functools import wraps
from config.logging import logger


def log_function_call(func):
    # Decorator to log function calls with parameters
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {e}")
            raise
    return wrapper


def log_operation(operation_name: str):
    # Decorator to log named operations
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Starting operation: {operation_name}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Operation completed: {operation_name}")
                return result
            except Exception as e:
                logger.error(f"Operation failed: {operation_name} - {e}")
                raise
        return wrapper
    return decorator


class LoggingContext:
    # Context manager for structured logging with additional context
    def __init__(self, context: Dict[str, Any]):
        self.context = context
        self.original_context = {}
    
    def __enter__(self):
        # Add context to logger (simplified implementation)
        logger.debug(f"Entering context: {self.context}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Remove context from logger
        if exc_type is not None:
            logger.error(f"Context error: {self.context} - {exc_val}")
        else:
            logger.debug(f"Exiting context: {self.context}")
        return False


def log_error_with_context(error: Exception, context: Dict[str, Any]):
    # Log error with additional context information
    logger.error(f"Error in context {context}: {str(error)}", extra={"context": context})
