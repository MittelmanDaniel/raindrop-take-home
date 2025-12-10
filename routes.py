"""API routes for the application."""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from models import NaturalLanguageQuery
from sql_generator import generate_sql_from_natural_language
from tinybird_client import execute_query

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    """Serve the HTML interface."""
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())


@router.post("/query")
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


@router.get("/schema")
async def get_schema():
    """Get schema information and basic data overview."""
    from sql_generator import SCHEMA_INFO
    from tinybird_client import execute_query
    
    try:
        # Get basic stats
        total_count_query = "SELECT count() as total FROM IBM_HR_Employee_Attrition FORMAT JSON"
        total_result = execute_query(total_count_query)
        total_rows = total_result.get('data', [{}])[0].get('total', 0) if total_result.get('data') else 0
        
        # Get department breakdown
        dept_query = "SELECT department, count() as count FROM IBM_HR_Employee_Attrition GROUP BY department FORMAT JSON"
        dept_result = execute_query(dept_query)
        departments = dept_result.get('data', [])
        
        # Parse schema info
        columns = []
        for line in SCHEMA_INFO.split('\n'):
            if line.strip().startswith('- '):
                col_info = line.strip()[2:]  # Remove '- '
                if '(' in col_info:
                    col_name = col_info.split('(')[0].strip()
                    col_type = col_info.split('(')[1].split(')')[0].strip()
                    columns.append({"name": col_name, "type": col_type})
        
        return {
            "columns": columns,
            "total_rows": total_rows,
            "departments": departments,
            "table_name": "IBM_HR_Employee_Attrition"
        }
    except Exception as e:
        return {
            "error": str(e),
            "columns": [],
            "total_rows": 0,
            "departments": []
        }


@router.get("/run-evals")
async def run_evals():
    """Run evaluation tests for CFG SQL generation."""
    from evals import run_all_evals
    
    try:
        all_passed = run_all_evals()
        return {
            "status": "success" if all_passed else "partial",
            "message": "Evals completed"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

