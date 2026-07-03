from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies.database import get_db
from services.dashboard_service import DashboardService
from schemas.dashboard import DashboardResponse
from config.logging import logger


router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/{dataset_id}", response_model=DashboardResponse)
async def get_dashboard(dataset_id: str, db: Session = Depends(get_db)):
    # Get dashboard with schema, relationships, and KPIs for a dataset
    try:
        dashboard_service = DashboardService(db)
        dashboard = dashboard_service.generate_dashboard(dataset_id)
        return dashboard
    except Exception as e:
        logger.error(f"Failed to generate dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate dashboard: {str(e)}"
        )
