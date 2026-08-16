from app.agent.clarification import classify_question
from app.agent.generator import generate_sql
from app.agent.validator import validate_sql
from app.database.connection import execute_query


def resolve_clarification(
    original_question: str,
    clarification_question: str,
    user_answer: str,
    provider: str = "groq",
):
    """
    Resolve a clarification response and continue
    to SQL generation.
    """

    combined_question = f"""
Original user question:
{original_question}

Clarification question:
{clarification_question}

User's clarification:
{user_answer}
"""

    print("\n========== COMBINED QUESTION ==========")
    print(combined_question)


    result = generate_sql(
        question=combined_question,
        provider=provider,
    )

    print("\n========== GENERATED SQL ==========")
    print(result.sql)


    validated_sql = validate_sql(result.sql)

    print("\n========== VALIDATED SQL ==========")
    print(validated_sql)


    database_result = execute_query(validated_sql)

    return {
        "status": "success",
        "sql": validated_sql,
        "explanation": result.explanation,
        "tables_used": result.tables_used,
        "data": database_result,
    }