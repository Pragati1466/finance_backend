from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
import uuid
from database.base import Base


class Dataset(Base):
    # Dataset model for storing uploaded file metadata
    __tablename__ = "datasets"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_format = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="uploading")
    row_count_total = Column(Integer, nullable=True)
    table_count = Column(Integer, nullable=True)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Table(Base):
    # Table model for storing individual table metadata within datasets
    __tablename__ = "tables"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String(36), nullable=False)
    table_name = Column(String(255), nullable=False)
    original_sheet_name = Column(String(255), nullable=True)
    row_count = Column(Integer, nullable=False)
    column_count = Column(Integer, nullable=False)
    duckdb_table_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Column(Base):
    # Column model for storing column metadata
    __tablename__ = "columns"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    table_id = Column(String(36), nullable=False)
    column_name = Column(String(255), nullable=False)
    data_type = Column(String(50), nullable=False)
    is_nullable = Column(String(10), nullable=False, default="true")
    is_primary_key = Column(String(10), nullable=False, default="false")
    sample_values = Column(Text, nullable=True)
    min_value = Column(String(50), nullable=True)
    max_value = Column(String(50), nullable=True)
    unique_count = Column(Integer, nullable=True)
    null_count = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
