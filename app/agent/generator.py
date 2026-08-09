from app.llm.manager import invoke_llm
from app.agent.prompt import SYSTEM_PROMPT


def generate_sql(
    question: str,
    provider: str = "groq",
) -> str:

    final_prompt = f"""
{SYSTEM_PROMPT}

USER QUESTION:
{question}

Return ONLY the PostgreSQL SELECT query.
"""

    return invoke_llm(
        prompt=final_prompt,
        provider=provider,
    )