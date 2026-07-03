from typing import Dict, List
from ai.llm.openai_client import openai_client
from ai.prompts.schema_analysis import SchemaAnalysisPrompts
from ai.parsers.response_parser import ResponseParser
from schemas.dashboard import TableSchema, ColumnSchema, RelationshipSchema
from config.logging import logger


class DashboardSchemaAnalyzer:
    # Handles AI-powered schema analysis for dashboard
    
    def analyze_schema(self, schema_summary: str) -> Dict:
        # Analyze schema using AI and convert to schema objects
        try:
            logger.info("Analyzing schema with AI")
            
            # Build prompt
            messages = SchemaAnalysisPrompts.build_schema_analysis_prompt(schema_summary)
            
            # Call AI
            response_text = openai_client.chat_completion(
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )
            
            # Parse response
            parsed = ResponseParser.extract_schema_analysis(response_text)
            
            # Convert to schema objects
            tables = self._convert_to_table_schemas(parsed["tables"])
            relationships = self._convert_to_relationship_schemas(parsed["relationships"])
            
            return {
                "tables": tables,
                "relationships": relationships,
                "financial_context": parsed["financial_context"]
            }
        except Exception as e:
            logger.error(f"Failed to analyze schema: {e}")
            raise
    
    def _convert_to_table_schemas(self, tables_data: List[Dict]) -> List[TableSchema]:
        # Convert raw table data to TableSchema objects
        return [
            TableSchema(
                name=table["name"],
                description=table["description"],
                columns=[
                    ColumnSchema(
                        name=col["name"],
                        type=col["type"],
                        meaning=col["meaning"],
                        is_primary_key=col["is_primary_key"],
                        is_foreign_key=col["is_foreign_key"],
                        references=col.get("references")
                    )
                    for col in table["columns"]
                ]
            )
            for table in tables_data
        ]
    
    def _convert_to_relationship_schemas(self, relationships_data: List[Dict]) -> List[RelationshipSchema]:
        # Convert raw relationship data to RelationshipSchema objects
        return [
            RelationshipSchema(
                source_table=rel["source_table"],
                source_column=rel["source_column"],
                target_table=rel["target_table"],
                target_column=rel["target_column"],
                relationship_type=rel["relationship_type"],
                confidence=rel["confidence"]
            )
            for rel in relationships_data
        ]
