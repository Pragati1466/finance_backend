from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies.database import get_db
from query.query_service import QueryService
from schemas.query import QueryRequest, QueryResponse
from config.logging import logger


router = APIRouter(prefix="/api/v1/query", tags=["query"])


@router.post("", response_model=QueryResponse)
async def process_query(request: QueryRequest, db: Session = Depends(get_db)):
    # Process conversational query and return results
    try:
        query_service = QueryService(db)
        response = query_service.process_query(request.dataset_id, request.question)
        return response
    except Exception as e:
        logger.error(f"Failed to process query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}"
        )
