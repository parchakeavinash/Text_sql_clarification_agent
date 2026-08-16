from app.llm.manager import get_llm
from app.agent.clarification_prompt import CLARIFICATION_PROMPT
from app.model import ClarificationResult

def classify_question(
    question: str,
    provider: str = 'groq',
)->ClarificationResult:
    
    llm = get_llm(provider)

    structured_llm = llm.with_structured_output(
        ClarificationResult
    )

    final_prompt = f"""
    {CLARIFICATION_PROMPT}

    USER QUESTION:
    {question}
    """
    result = structured_llm.invoke(final_prompt)

    return result