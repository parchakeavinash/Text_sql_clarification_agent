from dataclasses import field
from pydantic import BaseModel, Field
from typing import Literal

class SQLGenerationResult(BaseModel):
    sql: str = Field(
        description="A valid PostgreSQL SQL query that answers the user's question."
    )

    explanation: str = Field(
        description="A short explanation of what the SQL query does."
    )

    tables_used: list[str] = Field(
        description="List of database tables used in the SQL query."
    )

class ClarificationResult(BaseModel):
    classification: Literal[
        "clear",
        "ambiguous",
        "incomplete",
        "invalid",
    ] = Field(
        description="Classification of the user's question."
    )
    
    reasoning: str = Field(description="Brief explanation of why the question has this classification.")

    clarification_question : str = Field(default='',
    description="A concise clarification question. "
            "For clear or invalid questions, return an empty string.")
