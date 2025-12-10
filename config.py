"""Configuration management for the application."""
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def load_tinybird_config():
    """Load Tinybird configuration from .tinyb file."""
    with open('.tinyb', 'r') as f:
        config = json.load(f)
    return config['host'], config['token']

TINYBIRD_HOST, TINYBIRD_TOKEN = load_tinybird_config()
OPENAI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

