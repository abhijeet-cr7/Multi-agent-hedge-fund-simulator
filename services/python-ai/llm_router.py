from typing import Optional, Any
from langchain.schema import BaseMessage
from config import settings


def get_llm(provider: Optional[str] = None, **kwargs: Any):
    """
    Get an LLM instance with automatic fallback.
    Order: groq -> openai -> anthropic
    """
    provider = provider or settings.default_llm_provider

    if provider == "groq" and settings.groq_api_key:
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(
                api_key=settings.groq_api_key,
                model_name=kwargs.get("model", "llama3-8b-8192"),
                temperature=kwargs.get("temperature", 0.1),
            )
        except Exception:
            pass

    if provider == "openai" and settings.openai_api_key:
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                api_key=settings.openai_api_key,
                model=kwargs.get("model", "gpt-4-turbo-preview"),
                temperature=kwargs.get("temperature", 0.1),
            )
        except Exception:
            pass

    if provider == "anthropic" and settings.anthropic_api_key:
        try:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                api_key=settings.anthropic_api_key,
                model=kwargs.get("model", "claude-3-sonnet-20240229"),
                temperature=kwargs.get("temperature", 0.1),
            )
        except Exception:
            pass

    # Fallback: try any available provider
    for fallback_provider in ["groq", "openai", "anthropic"]:
        if fallback_provider == provider:
            continue
        result = get_llm(fallback_provider, **kwargs)
        if result is not None:
            return result

    return None


def route_llm(task_type: str = "default") -> Any:
    """
    Route to the best LLM based on task type.
    - cheap/fast: Groq (Llama)
    - high accuracy: OpenAI (GPT-4)
    - long reasoning: Anthropic (Claude)
    """
    routing = {
        "fast": "groq",
        "cheap": "groq",
        "accurate": "openai",
        "reasoning": "anthropic",
        "default": settings.default_llm_provider,
    }
    provider = routing.get(task_type, settings.default_llm_provider)
    return get_llm(provider)
