import os
from typing import Dict, Optional
from openai import OpenAI
from config.settings import settings
from config.logging import logger
from exceptions.exceptions import BaseApplicationError


class AIServiceError(BaseApplicationError):
    # Raised when AI service fails
    pass


class OpenAIClient:
    # Wrapper for OpenAI API with retry logic and error handling
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        self.model = "gpt-3.5-turbo"
        self.max_retries = 3
        self._initialized = False
    
    def _ensure_client(self):
        # Lazy initialization of OpenAI client
        if not self._initialized and self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self._initialized = True
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                raise AIServiceError(f"Failed to initialize OpenAI client: {str(e)}")
    
    def chat_completion(
        self,
        messages: list,
        temperature: float = 0.3,
        max_tokens: int = 2000,
        response_format: dict = None
    ) -> str:
        # Send chat completion request to OpenAI
        self._ensure_client()
        
        if not self.client:
            raise AIServiceError("OpenAI client not initialized. Please set OPENAI_API_KEY environment variable.")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise AIServiceError(f"AI service error: {str(e)}")
    
    def get_token_count(self, messages: list) -> int:
        # Estimate token count for messages
        total_chars = sum(len(str(msg.get("content", ""))) for msg in messages)
        return total_chars // 4  # Rough estimate: 4 chars per token


# Global OpenAI client instance
openai_client = OpenAIClient()
