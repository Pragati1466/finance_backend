from typing import Dict
from ai.llm.openai_client import openai_client
from config.logging import logger
from exceptions.exceptions import AIServiceError


class QueryLLMClient:
    # LLM client specialized for query generation
    
    def __init__(self):
        self.openai_client = openai_client
    
    def generate_sql(self, prompt: str) -> str:
        # Generate SQL query from natural language prompt
        try:
            logger.info("Generating SQL query using AI")
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a SQL expert specializing in financial data analysis. Generate accurate SQL queries based on the provided schema and user question. Return only the SQL query without explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            response = self.openai_client.chat_completion(
                messages=messages,
                temperature=0.1,
                max_tokens=500
            )
            
            logger.info("SQL query generated successfully")
            return response
        except AIServiceError as e:
            logger.error(f"Failed to generate SQL: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in SQL generation: {e}")
            raise AIServiceError(f"SQL generation failed: {str(e)}")
