from app.agent import clarification
from app.agent.clarification import classify_question
from app.agent.generator import generate_sql
from app.agent.validator import validate_sql
from app.database.connection import execute_query
from app.model import ConversationState

def run_agent(
    question: str,
    provider:str ='groq'
):
    """
    Run the Text-to-SQL clarification workflow.
    """
    # check the question
    clarification = classify_question(question,provider)

    print("\n========== CLASSIFICATION ==========")
    print(clarification.classification)

    print("\n========== REASONING ==========")
    print(clarification.reasoning)

    # handled invalid question

    if clarification.classification =='invalid':
        return {
            "status": "invalid",
            "message": (
                "Sorry, I cannot answer this question "
                "using the available e-commerce data."
            ),
        }

    # handled ambigious/incomplete question
    if clarification.classification in ["ambiguous","incomplete",]:
        return {
            'status': 'needs_clarification',
            'question':clarification.clarification_question,
        }

    # clear and generate sql query
    result = generate_sql(
        question=question,
        provider= provider,
    )
    # general sql query-> without validating 
    print("\n========== GENERATED SQL ==========")
    print(result.sql)

    # validate sql 
    validated_sql = validate_sql(result.sql)

    print("\n========== VALIDATED SQL ==========")
    print(validated_sql)


    # execute sql
    database_result = execute_query(validated_sql)
    return {
        "status": "success",
        "sql": validated_sql,
        "explanation": result.explanation,
        "tables_used": result.tables_used,
        "data": database_result,
    }