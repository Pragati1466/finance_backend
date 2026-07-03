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
from core.exceptions import handle_application_error, handle_generic_error
from exceptions.exceptions import FileSizeExceededError, InvalidFileTypeError


router = APIRouter(prefix="/api/v1/upload", tags=["upload"])


@router.post(
    "/demo",
    summary="Load Demo Dataset",
    description="Load a sample financial dataset for testing without uploading files",
    responses={
        200: {
            "description": "Demo dataset loaded successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Demo dataset loaded successfully",
                        "dataset_id": "uuid",
                        "status": "ready"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error"
        }
    }
)
async def load_demo_dataset(db: Session = Depends(get_db)):
    # Load demo dataset from sample data
    try:
        import shutil
        from pathlib import Path
        
        # Copy sample file to uploads
        sample_file = Path("sample_data/financial_sample.csv")
        if not sample_file.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sample data file not found"
            )
        
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}_financial_sample.csv"
        file_path = upload_dir / unique_filename
        
        # Copy sample file
        shutil.copy(sample_file, file_path)
        
        # Get file size
        file_size = file_path.stat().st_size
        
        # Create dataset record
        dataset_service = DatasetService(db)
        result = dataset_service.create_dataset(
            name="Demo Financial Dataset",
            original_filename="financial_sample.csv",
            file_format="csv",
            file_path=str(file_path),
            file_size=file_size
        )
        
        # Process dataset
        processed = dataset_service.process_dataset(result["dataset_id"])
        
        return {
            "message": "Demo dataset loaded successfully",
            "dataset_id": result["dataset_id"],
            "status": processed["status"]
        }
    except Exception as e:
        logger.error(f"Failed to load demo dataset: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load demo dataset: {str(e)}"
        )


@router.post(
    "/",
    summary="Upload File",
    description="Upload a CSV or Excel file for financial analysis",
    responses={
        200: {
            "description": "File uploaded successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "File uploaded and processed successfully",
                        "dataset_id": "uuid",
                        "status": "ready"
                    }
                }
            }
        },
        400: {
            "description": "Invalid file type or validation error"
        },
        413: {
            "description": "File size exceeds limit"
        },
        500: {
            "description": "Internal server error"
        }
    }
)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Handle file upload, validate, and trigger processing
    try:
        # Validate file size
        file_size = 0
        file_content = await file.read()
        file_size = len(file_content)
        max_size_bytes = settings.max_file_size_mb * 1024 * 1024
        
        if file_size > max_size_bytes:
            raise FileSizeExceededError(settings.max_file_size_mb)
        
        # Validate file type
        file_extension = Path(file.filename).suffix.lower().replace(".", "")
        allowed_types = settings.allowed_file_types.split(",")
        
        if file_extension not in allowed_types:
            raise InvalidFileTypeError(file_extension)
        
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
            
            # Process dataset synchronously for now (will be async in production)
            processed = dataset_service.process_dataset(result["dataset_id"])
            
            return {
                "message": "File uploaded and processed successfully",
                "dataset_id": result["dataset_id"],
                "status": processed["status"]
            }
        except Exception as e:
            logger.error(f"Failed to process dataset: {e}")
            # Clean up file if processing failed
            if file_path.exists():
                os.remove(file_path)
            raise handle_generic_error(e)
            
    except (FileSizeExceededError, InvalidFileTypeError) as e:
        raise handle_application_error(e)
    except HTTPException:
        raise
    except Exception as e:
        raise handle_generic_error(e)
