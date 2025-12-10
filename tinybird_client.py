"""Tinybird API client for executing SQL queries."""
import requests
from config import TINYBIRD_HOST, TINYBIRD_TOKEN


def execute_query(query: str) -> dict:
    """
    Execute a SQL query against Tinybird.
    
    Args:
        query: SQL query string
        
    Returns:
        dict: JSON response from Tinybird
        
    Raises:
        Exception: If the API request fails
    """
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

