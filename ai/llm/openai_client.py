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
    # Wrapper for Groq API (OpenAI-compatible) with retry logic and error handling
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.openai_api_key
        self.client = None
        self.model = "llama-3.3-70b-versatile"
        self.max_retries = 3
        self._initialized = False
    
    def _ensure_client(self):
        # Lazy initialization of Groq client using OpenAI-compatible interface
        if not self._initialized and self.api_key:
            try:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.groq.com/openai/v1"
                )
                self._initialized = True
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                raise AIServiceError(f"Failed to initialize Groq client: {str(e)}")
    
    def chat_completion(
        self,
        messages: list,
        temperature: float = 0.3,
        max_tokens: int = 2000,
        response_format: dict = None
    ) -> str:
        # Send chat completion request to Groq
        self._ensure_client()
        
        if not self.client:
            raise AIServiceError("Groq client not initialized. Please set OPENAI_API_KEY environment variable.")
        
        try:
            kwargs = dict(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            # Groq supports response_format for json_object mode
            if response_format:
                kwargs["response_format"] = response_format
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise AIServiceError(f"AI service error: {str(e)}")
    
    def get_token_count(self, messages: list) -> int:
        # Estimate token count for messages
        total_chars = sum(len(str(msg.get("content", ""))) for msg in messages)
        return total_chars // 4  # Rough estimate: 4 chars per token


# Global OpenAI client instance
openai_client = OpenAIClient()
