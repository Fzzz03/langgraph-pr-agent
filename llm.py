"""
Single place to get an LLM client. Defaults to Groq's free tier
(fast + zero cost). Swap providers by changing LLM_PROVIDER in .env —
the rest of the codebase never touches this detail.
"""

import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()


def get_llm(temperature: float = 0.2):
    if PROVIDER == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY"),
        )

    if PROVIDER == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.1"),
            temperature=temperature,
        )

    if PROVIDER == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

    raise ValueError(f"Unknown LLM_PROVIDER: {PROVIDER}")
