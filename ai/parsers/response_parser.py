import json
from typing import Dict, List, Any
from config.logging import logger
from exceptions.exceptions import BaseApplicationError


class ParseError(BaseApplicationError):
    # Raised when response parsing fails
    pass


class ResponseParser:
    # Parse and validate LLM responses
    
    @staticmethod
    def parse_json_response(response_text: str) -> Dict:
        # Parse JSON response from LLM
        try:
            # Clean up response text (remove markdown code blocks if present)
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
            
            parsed = json.loads(cleaned_text)
            return parsed
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ParseError(f"Invalid JSON response: {str(e)}")
    
    @staticmethod
    def validate_schema_analysis(response: Dict) -> bool:
        # Validate schema analysis response structure
        required_keys = ["tables", "relationships", "financial_context"]
        
        for key in required_keys:
            if key not in response:
                logger.error(f"Missing required key in response: {key}")
                return False
        
        if not isinstance(response["tables"], list):
            logger.error("tables must be a list")
            return False
        
        if not isinstance(response["relationships"], list):
            logger.error("relationships must be a list")
            return False
        
        # Validate table structure
        for table in response["tables"]:
            if "name" not in table or "columns" not in table:
                logger.error("Table missing required fields")
                return False
        
        # Validate relationship structure
        for rel in response["relationships"]:
            required_rel_keys = ["source_table", "source_column", "target_table", "target_column"]
            for key in required_rel_keys:
                if key not in rel:
                    logger.error(f"Relationship missing required key: {key}")
                    return False
        
        return True
    
    @staticmethod
    def validate_kpi_response(response: Dict) -> bool:
        # Validate KPI generation response structure
        if "kpis" not in response:
            logger.error("Missing kpis in response")
            return False
        
        if not isinstance(response["kpis"], list):
            logger.error("kpis must be a list")
            return False
        
        # Validate KPI structure
        for kpi in response["kpis"]:
            required_keys = ["name", "description", "sql_query", "category"]
            for key in required_keys:
                if key not in kpi:
                    logger.error(f"KPI missing required key: {key}")
                    return False
        
        return True
    
    @staticmethod
    def extract_schema_analysis(response_text: str) -> Dict:
        # Parse and validate schema analysis response
        parsed = ResponseParser.parse_json_response(response_text)
        
        if not ResponseParser.validate_schema_analysis(parsed):
            raise ParseError("Invalid schema analysis structure")
        
        return parsed
    
    @staticmethod
    def extract_kpis(response_text: str) -> List[Dict]:
        # Parse and validate KPI response
        parsed = ResponseParser.parse_json_response(response_text)
        
        if not ResponseParser.validate_kpi_response(parsed):
            raise ParseError("Invalid KPI response structure")
        
        return parsed["kpis"]
