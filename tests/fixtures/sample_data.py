import pandas as pd
from typing import Dict
from pathlib import Path


class SampleDataGenerator:
    # Generate sample data for testing
    
    @staticmethod
    def create_sample_financial_data() -> pd.DataFrame:
        # Create sample financial data for testing
        data = {
            'date': pd.date_range(start='2024-01-01', periods=12, freq='M'),
            'revenue': [100000, 120000, 115000, 130000, 140000, 135000, 
                       150000, 160000, 155000, 170000, 180000, 175000],
            'expenses': [80000, 85000, 82000, 90000, 95000, 92000,
                        100000, 105000, 102000, 110000, 115000, 112000],
            'profit': [20000, 35000, 33000, 40000, 45000, 43000,
                     50000, 55000, 53000, 60000, 65000, 63000],
            'category': ['Sales'] * 6 + ['Services'] * 6
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def create_sample_customer_data() -> pd.DataFrame:
        # Create sample customer data for testing
        data = {
            'customer_id': range(1, 11),
            'name': [f'Customer {i}' for i in range(1, 11)],
            'email': [f'customer{i}@example.com' for i in range(1, 11)],
            'signup_date': pd.date_range(start='2024-01-01', periods=10, freq='W'),
            'total_spend': [1000 + i * 100 for i in range(10)]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def create_sample_csv_file(file_path: str) -> None:
        # Create sample CSV file for testing
        df = SampleDataGenerator.create_sample_financial_data()
        df.to_csv(file_path, index=False)
    
    @staticmethod
    def create_sample_excel_file(file_path: str) -> None:
        # Create sample Excel file for testing
        df = SampleDataGenerator.create_sample_financial_data()
        df.to_excel(file_path, index=False)


class TestConfig:
    # Test configuration constants
    
    SAMPLE_DATASET_ID = "test-dataset-123"
    SAMPLE_TABLE_NAME = "financial_data"
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_FILE_TYPES = ['csv', 'xlsx', 'xls']
    
    @staticmethod
    def get_test_file_path(filename: str) -> str:
        # Get absolute path for test files
        return str(Path(__file__).parent.parent.parent / "test_data" / filename)
