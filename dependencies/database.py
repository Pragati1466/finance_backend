from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config.settings import settings
from config.logging import logger
from database.base import Base
from models.dataset import Dataset, Table, Column

# Create SQLAlchemy engine
engine = create_engine(
    "sqlite:///./finance_metadata.db",
    echo=settings.debug,
    connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    # Dependency for getting database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Initialize database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
