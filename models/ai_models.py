from sqlalchemy import Column, String, Integer, DateTime, Text, Float
from sqlalchemy.sql import func
import uuid
from database.base import Base


class Relationship(Base):
    # Model for storing detected table relationships
    __tablename__ = "relationships"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String(36), nullable=False)
    source_table = Column(String(255), nullable=False)
    source_column = Column(String(255), nullable=False)
    target_table = Column(String(255), nullable=False)
    target_column = Column(String(255), nullable=False)
    relationship_type = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=False)
    detected_by = Column(String(50), nullable=False, default="ai")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class KPI(Base):
    # Model for storing generated KPIs
    __tablename__ = "kpis"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    sql_query = Column(Text, nullable=False)
    computed_value = Column(Float, nullable=True)
    execution_status = Column(String(50), nullable=False, default="pending")
    execution_message = Column(Text, nullable=True)
    is_cached = Column(String(10), nullable=False, default="false")
    computed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
