"""SQL generation from natural language using OpenAI."""
import re
from config import OPENAI_CLIENT


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
    Convert natural language to ClickHouse SQL using OpenAI.
    
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
3. Always ends with FORMAT JSON
4. Uses proper ClickHouse syntax
5. Matches the exact column names from the schema above

Return ONLY the SQL query, nothing else. Do not include any explanations or markdown formatting."""

    try:
        response = OPENAI_CLIENT.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a SQL expert specializing in ClickHouse. Generate only valid SQL queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        sql_query = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        sql_query = re.sub(r'^```sql\s*', '', sql_query, flags=re.IGNORECASE)
        sql_query = re.sub(r'^```\s*', '', sql_query, flags=re.IGNORECASE)
        sql_query = re.sub(r'```\s*$', '', sql_query, flags=re.IGNORECASE)
        sql_query = sql_query.strip()
        
        # Ensure FORMAT JSON is present
        if "FORMAT JSON" not in sql_query.upper():
            sql_query = sql_query.rstrip().rstrip(';') + " FORMAT JSON"
        
        return sql_query
            
    except Exception as e:
        raise Exception(f"Error generating SQL: {str(e)}")

