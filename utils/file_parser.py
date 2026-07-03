import pandas as pd
from pathlib import Path
from typing import Dict, List
from config.settings import settings
from config.logging import logger
from exceptions.exceptions import FileParseError, InvalidFileTypeError
from constants.constants import FILE_TYPE_CSV, FILE_TYPE_XLSX, FILE_TYPE_XLS


class FileParser:
    # Parses CSV and Excel files into pandas DataFrames
    
    def __init__(self):
        self.supported_types = settings.allowed_file_types.split(",")
    
    def validate_file_type(self, file_path: str):
        # Check if file type is supported
        file_extension = Path(file_path).suffix.lower().replace(".", "")
        
        if file_extension not in self.supported_types:
            raise InvalidFileTypeError(file_extension)
        
        return file_extension
    
    def parse_csv(self, file_path: str) -> Dict[str, pd.DataFrame]:
        # Parse CSV file into a DataFrame
        try:
            logger.info(f"Parsing CSV file: {file_path}")
            df = pd.read_csv(file_path)
            
            # Normalize column names
            df.columns = self._normalize_column_names(df.columns)
            
            # Remove empty rows and columns
            df = self._clean_dataframe(df)
            
            table_name = Path(file_path).stem
            return {table_name: df}
        except Exception as e:
            logger.error(f"Failed to parse CSV file: {e}")
            raise FileParseError(str(e))
    
    def parse_excel(self, file_path: str) -> Dict[str, pd.DataFrame]:
        # Parse Excel file into DataFrames (one per sheet)
        try:
            logger.info(f"Parsing Excel file: {file_path}")
            
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            dataframes = {}
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                
                # Normalize column names
                df.columns = self._normalize_column_names(df.columns)
                
                # Clean the dataframe
                df = self._clean_dataframe(df)
                
                # Use sheet name as table name, sanitized
                table_name = self._sanitize_table_name(sheet_name)
                dataframes[table_name] = df
            
            logger.info(f"Parsed {len(dataframes)} sheets from Excel file")
            return dataframes
        except Exception as e:
            logger.error(f"Failed to parse Excel file: {e}")
            raise FileParseError(str(e))
    
    def parse_file(self, file_path: str) -> Dict[str, pd.DataFrame]:
        # Parse file based on its type
        file_type = self.validate_file_type(file_path)
        
        if file_type == FILE_TYPE_CSV:
            return self.parse_csv(file_path)
        elif file_type in [FILE_TYPE_XLSX, FILE_TYPE_XLS]:
            return self.parse_excel(file_path)
        else:
            raise InvalidFileTypeError(file_type)
    
    def _normalize_column_names(self, columns: pd.Index) -> List[str]:
        # Normalize column names to lowercase with underscores
        normalized = []
        for col in columns:
            # Convert to string, lowercase, replace spaces with underscores
            normalized_col = str(col).lower().strip().replace(" ", "_")
            # Remove special characters
            normalized_col = "".join(c for c in normalized_col if c.isalnum() or c == "_")
            normalized.append(normalized_col)
        return normalized
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        # Remove completely empty rows and columns
        df = df.dropna(how="all")  # Remove empty rows
        df = df.loc[:, df.notna().any()]  # Remove empty columns
        return df
    
    def _sanitize_table_name(self, name: str) -> str:
        # Sanitize table name for database compatibility
        sanitized = str(name).lower().strip().replace(" ", "_")
        sanitized = "".join(c for c in sanitized if c.isalnum() or c == "_")
        return sanitized
    
    def extract_metadata(self, df: pd.DataFrame) -> Dict:
        # Extract metadata from a DataFrame
        metadata = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": []
        }
        
        for col in df.columns:
            col_metadata = {
                "name": col,
                "data_type": str(df[col].dtype),
                "is_nullable": df[col].isna().any(),
                "null_count": df[col].isna().sum(),
                "unique_count": df[col].nunique(),
                "sample_values": df[col].dropna().head(5).tolist()
            }
            
            # Add min/max for numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                col_metadata["min_value"] = df[col].min()
                col_metadata["max_value"] = df[col].max()
            
            metadata["columns"].append(col_metadata)
        
        return metadata
