from typing import List, Optional
from sqlalchemy.orm import Session
from models.dataset import Dataset, Table, Column
from repositories.base import BaseRepository


class DatasetRepository(BaseRepository[Dataset]):
    # Repository for dataset operations
    
    def __init__(self, session: Session):
        super().__init__(Dataset, session)
    
    def get_by_status(self, status: str) -> List[Dataset]:
        # Get datasets by status
        return self.session.query(Dataset).filter(Dataset.status == status).all()
    
    def create_table(self, **kwargs) -> Table:
        # Create a table record
        table = Table(**kwargs)
        self.session.add(table)
        self.session.commit()
        self.session.refresh(table)
        return table
    
    def get_tables_by_dataset(self, dataset_id: str) -> List[Table]:
        # Get all tables for a dataset
        return self.session.query(Table).filter(Table.dataset_id == dataset_id).all()
    
    def create_column(self, **kwargs) -> Column:
        # Create a column record
        column = Column(**kwargs)
        self.session.add(column)
        self.session.commit()
        self.session.refresh(column)
        return column
    
    def get_columns_by_table(self, table_id: str) -> List[Column]:
        # Get all columns for a table
        return self.session.query(Column).filter(Column.table_id == table_id).all()
    
    def update_status(self, dataset_id: str, status: str) -> Optional[Dataset]:
        # Update dataset status
        return self.update(dataset_id, status=status)
