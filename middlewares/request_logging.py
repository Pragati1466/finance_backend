import time
from fastapi import Request
from config.logging import logger


async def request_logging(request: Request, call_next):
    # Log all incoming requests with timing information
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log response
    logger.info(f"Response: {response.status_code} - Duration: {duration:.3f}s")
    
    return response
