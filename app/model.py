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
    ]
    

    reasoning: str

    clarification_question : str
# this will hold the converstation
class ConversationState(BaseModel):
    original_qestion: str
    clarification_question: str = ""
    clarification_answer: str = ""