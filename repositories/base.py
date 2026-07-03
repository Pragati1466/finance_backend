from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    # Base repository with common CRUD operations
    
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session
    
    def create(self, **kwargs) -> ModelType:
        # Create a new record
        db_obj = self.model(**kwargs)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def get_by_id(self, id: str) -> Optional[ModelType]:
        # Get a record by ID
        return self.session.query(self.model).filter(self.model.id == str(id)).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        # Get all records with pagination
        return self.session.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id: str, **kwargs) -> Optional[ModelType]:
        # Update a record by ID
        db_obj = self.get_by_id(id)
        if db_obj:
            for key, value in kwargs.items():
                setattr(db_obj, key, value)
            self.session.commit()
            self.session.refresh(db_obj)
        return db_obj
    
    def delete(self, id: str) -> bool:
        # Delete a record by ID
        db_obj = self.get_by_id(id)
        if db_obj:
            self.session.delete(db_obj)
            self.session.commit()
            return True
        return False
