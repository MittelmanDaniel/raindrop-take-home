"""SQL generation from natural language using OpenAI CFG."""
import os
from config import OPENAI_CLIENT


def load_grammar():
    """Load the ClickHouse SQL grammar from the .lark file."""
    grammar_path = os.path.join(os.path.dirname(__file__), 'clickhouse_sql.lark')
    with open(grammar_path, 'r') as f:
        return f.read()


CLICKHOUSE_SQL_GRAMMAR = load_grammar()


SCHEMA_INFO = """
Available columns in IBM_HR_Employee_Attrition table:
- _age (Int16)
- attrition (String: "Yes" or "No")
- businesstravel (String)
- dailyrate (Int32)
- department (String)
- distancefromhome (Int16)
- education (Int16)
- educationfield (String)
- employeecount (Int16)
- employeenumber (Int32)
- environmentsatisfaction (Int16)
- gender (String)
- hourlyrate (Int16)
- jobinvolvement (Int16)
- joblevel (Int16)
- jobrole (String)
- jobsatisfaction (Int16)
- maritalstatus (String)
- monthlyincome (Int32)
- monthlyrate (Int32)
- numcompaniesworked (Int16)
- over18 (String)
- overtime (String: "Yes" or "No")
- percentsalaryhike (Int16)
- performancerating (Int16)
- relationshipsatisfaction (Int16)
- standardhours (Int16)
- stockoptionlevel (Int16)
- totalworkingyears (Int16)
- trainingtimeslastyear (Int16)
- worklifebalance (Int16)
- yearsatcompany (Int16)
- yearsincurrentrole (Int16)
- yearssincelastpromotion (Int16)
- yearswithcurrmanager (Int16)
"""


def generate_sql_from_natural_language(natural_language_query: str) -> str:
    """
    Convert natural language to ClickHouse SQL using OpenAI CFG.
    
    Args:
        natural_language_query: Natural language question
        
    Returns:
        str: Generated SQL query
        
    Raises:
        Exception: If SQL generation fails
    """
    prompt = f"""Convert the following natural language query into a ClickHouse SQL query for the IBM HR Employee Attrition dataset.

{SCHEMA_INFO}

Natural language query: {natural_language_query}

Generate a valid ClickHouse SQL query that:
1. Uses SELECT statements only (read-only queries)
2. Queries from the table: IBM_HR_Employee_Attrition
3. Uses proper ClickHouse syntax
4. Matches the exact column names from the schema above

The grammar will automatically add FORMAT JSON to the query.

YOU MUST REASON HEAVILY ABOUT THE QUERY AND MAKE SURE IT OBEYS THE GRAMMAR."""

    try:
        response = OPENAI_CLIENT.responses.create(
            model="gpt-5.1",
            input=prompt,
            text={"format": {"type": "text"}},
            tools=[
                {
                    "type": "custom",
                    "name": "clickhouse_sql_grammar",
                    "description": "Generates read-only ClickHouse SQL queries for the IBM_HR_Employee_Attrition table. Only SELECT statements are allowed. Always end queries with FORMAT JSON. YOU MUST REASON HEAVILY ABOUT THE QUERY AND MAKE SURE IT OBEYS THE GRAMMAR.",
                    "format": {
                        "type": "grammar",
                        "syntax": "lark",
                        "definition": CLICKHOUSE_SQL_GRAMMAR
                    }
                },
            ],
            parallel_tool_calls=False
        )
        
        # Extract the SQL query from the tool call
        sql_query = None
        for item in response.output:
            if hasattr(item, 'input'):
                sql_query = item.input
                break
        
        if not sql_query:
            raise Exception("Failed to generate SQL query from OpenAI response - no tool call found")
        
        # Ensure FORMAT JSON is present (safety check, though grammar should enforce it)
        sql_query = sql_query.strip()
        if "FORMAT JSON" not in sql_query.upper():
            sql_query = sql_query.rstrip().rstrip(';') + " FORMAT JSON"
        
        return sql_query
            
    except Exception as e:
        raise Exception(f"Error generating SQL: {str(e)}")

