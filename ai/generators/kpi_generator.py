from typing import List, Dict
from ai.llm.openai_client import openai_client
from ai.prompts.schema_analysis import SchemaAnalysisPrompts
from ai.parsers.response_parser import ResponseParser
from config.logging import logger


class KPIGenerator:
    # Generate financial KPIs using AI
    
    def __init__(self):
        self.openai_client = openai_client
        self.prompt_builder = SchemaAnalysisPrompts()
        self.response_parser = ResponseParser()
    
    def generate_kpis(self, schema_summary: str, financial_context: str) -> List[Dict]:
        # Generate KPIs based on schema and financial context
        try:
            logger.info("Generating KPIs using AI")
            
            # Build prompt
            messages = self.prompt_builder.build_kpi_generation_prompt(
                schema_summary,
                financial_context
            )
            
            # Call AI
            response_text = self.openai_client.chat_completion(
                messages=messages,
                temperature=0.5,
                max_tokens=2000
            )
            
            # Parse response
            kpis = self.response_parser.extract_kpis(response_text)
            
            logger.info(f"Generated {len(kpis)} KPIs")
            return kpis
        except Exception as e:
            logger.error(f"Failed to generate KPIs: {e}")
            raise
