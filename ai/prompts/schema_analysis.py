from typing import Dict, List


class SchemaAnalysisPrompts:
    # Prompt templates for schema analysis
    
    @staticmethod
    def build_schema_analysis_prompt(schema_summary: str) -> List[Dict]:
        # Build prompt for analyzing database schema
        system_prompt = {
            "role": "system",
            "content": """You are a financial data analyst specializing in database schema analysis. 
            Analyze the provided table schemas and provide insights about relationships, 
            primary keys, foreign keys, and financial context. Return your response in JSON format."""
        }
        
        user_prompt = {
            "role": "user",
            "content": f"""Analyze the following database schema and provide:

1. Table descriptions for each table
2. Column meanings and data types
3. Relationships between tables (identify primary keys and foreign keys)
4. Join suggestions for common queries
5. Financial context and business insights

Schema Summary:
{schema_summary}

Return the response in this JSON format:
{{
    "tables": [
        {{
            "name": "table_name",
            "description": "table description",
            "columns": [
                {{
                    "name": "column_name",
                    "type": "data_type",
                    "meaning": "column meaning",
                    "is_primary_key": true/false,
                    "is_foreign_key": true/false,
                    "references": "referenced_table.column if foreign key"
                }}
            ]
        }}
    ],
    "relationships": [
        {{
            "source_table": "table1",
            "source_column": "column1",
            "target_table": "table2",
            "target_column": "column2",
            "relationship_type": "one_to_one/one_to_many/many_to_many",
            "confidence": 0.0-1.0
        }}
    ],
    "financial_context": "overall financial context and business insights"
}}"""
        }
        
        return [system_prompt, user_prompt]
    
    @staticmethod
    def build_kpi_generation_prompt(schema_summary: str, financial_context: str) -> List[Dict]:
        # Build prompt for generating financial KPIs
        system_prompt = {
            "role": "system",
            "content": """You are a financial metrics expert specializing in KPI generation. 
            Analyze the provided schema and suggest 10-15 relevant financial KPIs that can be 
            calculated from the data. Return your response in JSON format."""
        }
        
        user_prompt = {
            "role": "user",
            "content": f"""Based on the following database schema and financial context, 
            suggest 10-15 useful financial KPIs that can be calculated.

Schema Summary:
{schema_summary}

Financial Context:
{financial_context}

For each KPI, provide:
1. Name of the KPI
2. Description of what it measures
3. SQL query to calculate it (using actual table and column names)
4. Category (profitability, liquidity, efficiency, growth, valuation)

Common financial KPIs to consider:
- Revenue, MRR, CAC, Burn Rate, Customer Churn
- Gross Margin, Net Profit, Expense Ratio
- Monthly Growth, Customer Lifetime Value
- Current Ratio, Quick Ratio, Asset Turnover
- ROE, ROA, P/E Ratio

Return the response in this JSON format:
{{
    "kpis": [
        {{
            "name": "KPI Name",
            "description": "What this KPI measures",
            "sql_query": "SELECT ... FROM ...",
            "category": "profitability/liquidity/efficiency/growth/valuation"
        }}
    ]
}}"""
        }
        
        return [system_prompt, user_prompt]
