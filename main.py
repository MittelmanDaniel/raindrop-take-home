from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
import requests
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()

def load_tinybird_config():
    with open('.tinyb', 'r') as f:
        config = json.load(f)
    return config['host'], config['token']

TINYBIRD_HOST, TINYBIRD_TOKEN = load_tinybird_config()
OPENAI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sql_from_natural_language(natural_language_query: str) -> str:
    """
    Convert natural language to ClickHouse SQL using OpenAI.
    """
    schema_info = """
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
    
    prompt = f"""Convert the following natural language query into a ClickHouse SQL query for the IBM HR Employee Attrition dataset.

{schema_info}

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
            model="gpt-4o-mini",  # Using a more stable model
            messages=[
                {"role": "system", "content": "You are a SQL expert specializing in ClickHouse. Generate only valid SQL queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1  # Low temperature for more deterministic output
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

def execute_query(query: str):
    """Execute a SQL query against Tinybird."""
    # Ensure FORMAT JSON is in the query
    query = query.strip()
    if "FORMAT" not in query.upper():
        query = query.rstrip().rstrip(';') + " FORMAT JSON"
    
    url = f"{TINYBIRD_HOST}/v0/sql"
    headers = {
        "Authorization": f"Bearer {TINYBIRD_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "q": query
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"Tinybird API error: {response.status_code}, {response.text}")
    
    return response.json()

class NaturalLanguageQuery(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the HTML interface."""
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/query")
async def natural_language_query(request: NaturalLanguageQuery):
    """
    Convert natural language to SQL and execute it against Tinybird.
    
    Example: {"query": "How many employees are in Sales department?"}
    """
    try:
        # Step 1: Convert natural language to SQL
        sql_query = generate_sql_from_natural_language(request.query)
        
        # Step 2: Execute the SQL query
        results = execute_query(sql_query)
        
        return {
            "natural_language_query": request.query,
            "generated_sql": sql_query,
            "results": results
        }
    except Exception as e:
        return {
            "error": str(e),
            "natural_language_query": request.query
        }
    
