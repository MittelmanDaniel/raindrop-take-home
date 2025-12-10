"""Configuration management for the application."""
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def load_tinybird_config():
    """
    Load Tinybird configuration from environment variables or .tinyb file.
    Environment variables take precedence (for production deployments).
    """
    # Try environment variables first (for Vercel/production)
    host = os.getenv("TINYBIRD_HOST")
    token = os.getenv("TINYBIRD_TOKEN")
    
    # Fall back to .tinyb file if env vars not set (for local development)
    if not host or not token:
        try:
            with open('.tinyb', 'r') as f:
                config = json.load(f)
            host = host or config.get('host')
            token = token or config.get('token')
        except FileNotFoundError:
            pass
    
    if not host or not token:
        raise ValueError(
            "Tinybird configuration not found. "
            "Set TINYBIRD_HOST and TINYBIRD_TOKEN environment variables, "
            "or ensure .tinyb file exists."
        )
    
    return host, token

TINYBIRD_HOST, TINYBIRD_TOKEN = load_tinybird_config()
OPENAI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

