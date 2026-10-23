from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_MODEL, GOOGLE_API_KEY, TEMPERATURE, validate_config


def get_llm() -> ChatGoogleGenerativeAI:
    """Create the shared Gemini client."""
    validate_config()
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=TEMPERATURE,
    )


def get_structured_llm(schema):
    """Create a Gemini client that returns data matching a Pydantic model."""
    return get_llm().with_structured_output(schema)