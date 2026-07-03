from typing import Dict, List
from config.logging import logger


class PromptBuilder:
    # Build prompts for SQL generation with context
    
    def build_query_prompt(
        self,
        question: str,
        schema_summary: str,
        relationships: List[Dict],
        kpi_context: str = ""
    ) -> str:
        # Build comprehensive prompt for SQL generation
        try:
            prompt = f"""You are a SQL expert for financial data analysis. Generate a SQL query to answer the user's question.

DATABASE SCHEMA:
{schema_summary}

TABLE RELATIONSHIPS:
{self._format_relationships(relationships)}

AVAILABLE KPIS AND METRICS:
{kpi_context if kpi_context else "No specific KPI context available."}

USER QUESTION:
{question}

REQUIREMENTS:
1. Use the actual table and column names from the schema
2. Use appropriate JOINs based on the relationships
3. Return only the SQL query, no explanations
4. Use DuckDB SQL syntax
5. Handle NULL values appropriately
6. Use proper aggregation when needed
7. Limit results to 100 rows for performance

Generate the SQL query:"""
            
            logger.info("Query prompt built successfully")
            return prompt
        except Exception as e:
            logger.error(f"Failed to build prompt: {e}")
            raise
    
    def _format_relationships(self, relationships: List[Dict]) -> str:
        # Format relationships for prompt readability
        if not relationships:
            return "No relationships detected."
        
        formatted = []
        for rel in relationships:
            formatted.append(
                f"- {rel['source_table']}.{rel['source_column']} -> "
                f"{rel['target_table']}.{rel['target_column']} "
                f"({rel['relationship_type']})"
            )
        
        return "\n".join(formatted)
