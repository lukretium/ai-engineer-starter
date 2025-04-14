from app.core.config import settings
from app.llm.anthropic import AnthropicLLM
from app.llm.base import LLM
from app.llm.ollama import OllamaLLM
from app.llm.openai import OpenAILLM


class LLMFactory:
    @staticmethod
    def create_llm() -> LLM:
        llm_type = settings.LLM_TYPE.lower()

        if llm_type == "openai":
            return OpenAILLM(
                api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_MODEL
            )
        elif llm_type == "anthropic":
            return AnthropicLLM(
                api_key=settings.ANTHROPIC_API_KEY, model=settings.ANTHROPIC_MODEL
            )
        elif llm_type == "ollama":
            return OllamaLLM(
                model=settings.OLLAMA_MODEL, base_url=settings.OLLAMA_BASE_URL
            )
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")
