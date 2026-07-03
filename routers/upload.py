import os
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.settings import settings
from config.logging import logger
from dependencies.database import get_db
from services.dataset_service import DatasetService
from schemas.dataset import DatasetResponse
from exceptions.exceptions import FileSizeExceededError, InvalidFileTypeError


router = APIRouter(prefix="/api/v1/upload", tags=["upload"])


@router.post("/", response_model=dict)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Handle file upload, validate, and trigger processing
    
    # Validate file size
    file_size = 0
    file_content = await file.read()
    file_size = len(file_content)
    max_size_bytes = settings.max_file_size_mb * 1024 * 1024
    
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {settings.max_file_size_mb}MB"
        )
    
    # Validate file type
    file_extension = Path(file.filename).suffix.lower().replace(".", "")
    allowed_types = settings.allowed_file_types.split(",")
    
    if file_extension not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {settings.allowed_file_types}"
        )
    
    # Create upload directory if it doesn't exist
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = upload_dir / unique_filename
    
    # Save file
    try:
        with open(file_path, "wb") as f:
            f.write(file_content)
        logger.info(f"File saved to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save file"
        )
    
    # Create dataset record
    dataset_service = DatasetService(db)
    try:
        result = dataset_service.create_dataset(
            name=file.filename,
            original_filename=file.filename,
            file_format=file_extension,
            file_path=str(file_path),
            file_size=file_size
        )
        
        # Process dataset synchronously for now (will be_ASYNC in production)
        dataset_service.process_dataset(result["dataset_id"])
        
        return {
            "message": "File uploaded and processed successfully",
            "dataset_id": result["dataset_id"],
            "status": result["status"]
        }
    except Exception as e:
        logger.error(f"Failed to process dataset: {e}")
        # Clean up file if processing failed
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )
