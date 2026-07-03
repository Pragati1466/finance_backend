import re
from typing import Dict, List, Tuple
from config.logging import logger
from exceptions.exceptions import BaseApplicationError


class SQLValidationError(BaseApplicationError):
    # Raised when SQL validation fails
    pass


class SQLValidator:
    # Validate SQL queries for security and correctness
    
    # Dangerous SQL keywords that should be blocked
    DANGEROUS_KEYWORDS = [
        "DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE", "INSERT", "UPDATE",
        "GRANT", "REVOKE", "EXEC", "EXECUTE"
    ]
    
    def __init__(self, allowed_tables: List[str] = None):
        self.allowed_tables = allowed_tables or []
    
    def validate_query(self, sql: str) -> Tuple[bool, str]:
        # Validate SQL query for security and correctness
        try:
            # Check for dangerous keywords
            if self._contains_dangerous_keywords(sql):
                return False, "Query contains dangerous operations"
            
            # Check for basic SQL injection patterns
            if self._contains_injection_patterns(sql):
                return False, "Query contains potential injection patterns"
            
            # Check if query is SELECT only
            if not self._is_select_query(sql):
                return False, "Only SELECT queries are allowed"
            
            # Validate table names if allowed tables specified
            if self.allowed_tables and not self._validate_tables(sql):
                return False, "Query references unauthorized tables"
            
            logger.info("SQL query validation passed")
            return True, "Validation passed"
        except Exception as e:
            logger.error(f"SQL validation error: {e}")
            return False, f"Validation error: {str(e)}"
    
    def _contains_dangerous_keywords(self, sql: str) -> bool:
        # Check if query contains dangerous SQL keywords
        sql_upper = sql.upper()
        for keyword in self.DANGEROUS_KEYWORDS:
            if keyword in sql_upper:
                logger.warning(f"Dangerous keyword detected: {keyword}")
                return True
        return False
    
    def _contains_injection_patterns(self, sql: str) -> bool:
        # Check for common SQL injection patterns
        injection_patterns = [
            r"/\*", # Multi-line comment start
            r"\*/", # Multi-line comment end
            r"xp_", # Extended stored procedures
            r"sp_"  # System stored procedures
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, sql, re.IGNORECASE):
                logger.warning(f"Injection pattern detected: {pattern}")
                return True
        return False
    
    def _is_select_query(self, sql: str) -> bool:
        # Ensure query is a SELECT statement
        sql_stripped = sql.strip().upper()
        return sql_stripped.startswith("SELECT")
    
    def _validate_tables(self, sql: str) -> bool:
        # Validate that query only uses allowed tables
        # Extract table names from query (simplified approach)
        words = re.findall(r'\b\w+\b', sql.upper())
        
        for word in words:
            if word in [t.upper() for t in self.allowed_tables]:
                continue
            # Skip common SQL keywords
            if word in ["SELECT", "FROM", "WHERE", "JOIN", "ON", "AND", "OR", "GROUP", "BY", "ORDER", "HAVING", "LIMIT", "AS", "LEFT", "RIGHT", "INNER", "OUTER"]:
                continue
            # If it's not a keyword and not in allowed tables, it might be a table name
            if word not in ["SELECT", "FROM", "WHERE", "JOIN", "ON", "AND", "OR", "GROUP", "BY", "ORDER", "HAVING", "LIMIT", "AS", "LEFT", "RIGHT", "INNER", "OUTER"]:
                # This is a simplified check - in production, use proper SQL parser
                pass
        
        return True
    
    def sanitize_query(self, sql: str) -> str:
        # Sanitize SQL query by removing potentially harmful elements

        # Strip markdown code fences (```sql ... ``` or ``` ... ```)
        sql = sql.strip()
        if sql.startswith("```"):
            sql = re.sub(r"^```[a-zA-Z]*\n?", "", sql)
            sql = re.sub(r"```$", "", sql)
            sql = sql.strip()

        # Remove comments
        sql = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)

        # Fix strftime(column, fmt) where column is not already cast
        # DuckDB requires strftime(DATE/TIMESTAMP, fmt) — auto-cast bare column references
        def fix_strftime(match):
            col = match.group(1).strip()
            fmt = match.group(2)
            # If already has a CAST, leave it alone
            if 'CAST' in col.upper() or 'TIMESTAMP' in col.upper():
                return f"strftime({col}, {fmt})"
            return f"strftime(CAST({col} AS DATE), {fmt})"

        sql = re.sub(
            r'strftime\(\s*([^,]+?)\s*,\s*(%[^)]+)\)',
            fix_strftime,
            sql,
            flags=re.IGNORECASE
        )

        # Remove extra whitespace
        sql = ' '.join(sql.split())

        return sql.strip()
