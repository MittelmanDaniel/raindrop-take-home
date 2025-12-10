"""Pydantic models for API requests and responses."""
from pydantic import BaseModel


class NaturalLanguageQuery(BaseModel):
    """Request model for natural language queries."""
    query: str

