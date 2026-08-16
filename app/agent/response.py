from app.llm.manager import generate_response

RESPONSE_PROMPT = """
    You are the final answer generator for a Text-to-SQL system.

    Your task is to answer the user's original question using ONLY
    the database result provided to you.

    User question:
    {question}

    SQL query:
    {sql}

    Database result:
    {result}
    Rules:
    - Answer the user's question directly.
    - Use only the database result.
    - Never invent information.
    - Never modify or contradict the result.
    - Do not mention the SQL query.
    - Do not mention the LLM, agent, or internal processing.
    - Keep the answer concise.
    - Format numbers, currency, dates, and lists naturally.
    - If the result is empty, clearly state that no matching records were found.
    """


def generate_natural_language_response(
    question: str,
    sql: str,
    result,
    provider: str = "groq"
) ->str: 

    prompt = RESPONSE_PROMPT.format(
        question=question,
        sql=sql,
        result=result,
    )

    return generate_response(
        prompt=prompt,
        provider=provider,
    )
