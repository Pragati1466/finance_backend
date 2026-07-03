from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies.database import get_db
from query.query_service import QueryService
from schemas.query import QueryRequest, QueryResponse
from config.logging import logger


router = APIRouter(prefix="/api/v1/query", tags=["query"])


@router.post(
    "",
    response_model=QueryResponse,
    summary="Process Query",
    description="Process natural language queries against uploaded datasets using AI-powered SQL generation",
    responses={
        200: {
            "description": "Query processed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "question": "What is the total revenue?",
                        "sql_query": "SELECT SUM(revenue) FROM data",
                        "results": [],
                        "explanation": "This query calculates total revenue"
                    }
                }
            }
        },
        400: {
            "description": "Invalid request"
        },
        404: {
            "description": "Dataset not found"
        },
        500: {
            "description": "Internal server error"
        }
    }
)
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
