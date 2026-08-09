from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

from config.env_variable import settings


groq_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.GROQ_API_KEY,
    temperature=0,
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    api_key=settings.GEMINI_API_KEY,
    temperature=0,
)