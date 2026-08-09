from app.llm.provider import groq_llm,gemini_llm

def invoke_llm(prompt:str,provider: str ='groq',) ->str:
    """
    Invoke an LLM.
    groq:
        Groq → Gemini fallback
    gemini:
        Gemini only
    """

    if provider =='gemini':
        response = gemini_llm.invoke(prompt)
        return response.content

    if provider =='groq':
        try:
            response = groq_llm.invoke(prompt)
            return response.content

        except Exception as groq_error:
            print(f'Groq failed: {groq_error}')
            print('falling back to gemini...')

            try:
                response = gemini_llm.invoke(prompt)
                return response.content
            except Exception as gemini_error:
                
                raise RuntimeError(
                    "Both Groq and gemini failed..."
                )from gemini_error

    raise ValueError(
            "provider must be either 'groq" or 'gemini'
    )

    