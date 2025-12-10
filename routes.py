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

