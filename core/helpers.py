from typing import Any, Dict, List, Optional
from datetime import datetime
import pandas as pd


def format_timestamp(dt: datetime) -> str:
    # Format datetime to ISO string
    return dt.isoformat()


def sanitize_string(value: str) -> str:
    # Sanitize string input by stripping whitespace
    return value.strip() if value else ""


def safe_float(value: Any) -> Optional[float]:
    # Safely convert value to float, return None if conversion fails
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None


def safe_int(value: Any) -> Optional[int]:
    # Safely convert value to int, return None if conversion fails
    try:
        return int(value) if value is not None else None
    except (ValueError, TypeError):
        return None


def truncate_string(value: str, max_length: int = 100) -> str:
    # Truncate string to max length with ellipsis
    if not value or len(value) <= max_length:
        return value
    return value[:max_length - 3] + "..."


def is_empty(value: Any) -> bool:
    # Check if value is empty (None, empty string, empty list, etc.)
    if value is None:
        return True
    if isinstance(value, (str, list, dict)) and len(value) == 0:
        return True
    return False


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    # Merge multiple dictionaries, later dicts override earlier ones
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def extract_nested_value(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    # Extract nested value from dictionary using key path
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def convert_dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
    # Convert pandas DataFrame to list of dictionaries
    return df.to_dict("records") if not df.empty else []


def validate_positive_number(value: Any, field_name: str = "value") -> Optional[float]:
    # Validate that value is a positive number
    num = safe_float(value)
    if num is not None and num < 0:
        raise ValueError(f"{field_name} must be positive")
    return num


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    # Split list into chunks of specified size
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
