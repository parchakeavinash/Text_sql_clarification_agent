from app.llm.provider import groq_llm, gemini_llm


def get_llm(provider: str = "groq"):
    """Return an LLM instance."""

    if provider == "groq":
        return groq_llm

    if provider == "gemini":
        return gemini_llm

    raise ValueError(
        "provider must be either 'groq' or 'gemini'"
    )

def generate_response(
    prompt:str,
    provider: str = "groq",
)->str:

    llm = groq_llm if provider == "groq" else gemini_llm

    try:
        response = llm.invoke(prompt)

        return response.content.strip()

    except Exception as primary_error:

        if provider == "groq":
            try:
                response = gemini_llm.invoke(prompt)
                return response.content.strip()

            except Exception as fallback_error:
                raise RuntimeError(
                    f"LLM generation failed. "
                    f"Primary error: {primary_error}; "
                    f"Fallback error: {fallback_error}"
                )

        raise RuntimeError(
            f"LLM generation failed: {primary_error}"
        )


def invoke_llm(prompt: str, provider: str = "groq") -> str:
    """Invoke an LLM and return text."""

    if provider == "gemini":
        response = gemini_llm.invoke(prompt)
        return response.content

    if provider == "groq":
        try:
            response = groq_llm.invoke(prompt)
            return response.content

        except Exception as groq_error:
            print(f"Groq failed: {groq_error}")
            print("Falling back to Gemini...")

            try:
                response = gemini_llm.invoke(prompt)
                return response.content

            except Exception as gemini_error:
                raise RuntimeError(
                    "Both Groq and Gemini failed."
                ) from gemini_error

    raise ValueError(
        "provider must be either 'groq' or 'gemini'"
    )