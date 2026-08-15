from app.llm.manager import get_llm
from app.agent.prompt import SYSTEM_PROMPT
from app.model import SQLGenerationResult


def generate_sql(
    question: str,
    provider: str = "groq",
) -> SQLGenerationResult:

    llm = get_llm(provider)

    structured_llm = llm.with_structured_output(
        SQLGenerationResult
    )

    final_prompt = f"""
    {SYSTEM_PROMPT}

    USER QUESTION:
    {question}
    """

    result = structured_llm.invoke(final_prompt)

    return result