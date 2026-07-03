from typing import Dict, Any, List
from config.logging import logger


class ResponseFormatter:
    # Format query responses for API consumption
    
    def format_query_response(
        self,
        question: str,
        generated_sql: str,
        query_result: Dict[str, Any],
        validation_status: bool = True,
        validation_message: str = ""
    ) -> Dict[str, Any]:
        # Format complete query response
        try:
            response = {
                "question": question,
                "generated_sql": generated_sql,
                "query_result": {
                    "success": query_result["success"],
                    "row_count": query_result["row_count"],
                    "data": query_result["data"] if query_result["success"] else [],
                    "message": query_result["message"]
                },
                "validation": {
                    "passed": validation_status,
                    "message": validation_message
                },
                "explanation": self._generate_explanation(
                    question,
                    query_result,
                    validation_status
                )
            }
            
            logger.info("Query response formatted successfully")
            return response
        except Exception as e:
            logger.error(f"Failed to format response: {e}")
            raise
    
    def _generate_explanation(
        self,
        question: str,
        query_result: Dict[str, Any],
        validation_passed: bool
    ) -> str:
        # Generate natural language explanation of results
        if not validation_passed:
            return "The generated query could not be validated for safety reasons."
        
        if not query_result["success"]:
            return f"The query could not be executed: {query_result['message']}"
        
        if query_result["row_count"] == 0:
            return "The query executed successfully but returned no results. This might indicate no data matches your criteria."
        
        if query_result["row_count"] == 1:
            return f"The query returned 1 result matching your question."
        
        return f"The query returned {query_result['row_count']} results matching your question."
    
    def format_error_response(self, question: str, error_message: str) -> Dict[str, Any]:
        # Format error response for failed queries
        return {
            "question": question,
            "generated_sql": None,
            "query_result": {
                "success": False,
                "row_count": 0,
                "data": [],
                "message": error_message
            },
            "validation": {
                "passed": False,
                "message": "Query generation or execution failed"
            },
            "explanation": f"Unable to answer your question: {error_message}"
        }
