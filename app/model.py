from pydantic import BaseModel, Field


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