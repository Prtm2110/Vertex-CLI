"""Google Gemini provider implementation using LangChain."""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models import BaseChatModel
from cli.models.base_provider import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider."""

    def _create_llm(self) -> BaseChatModel:
        kwargs = {
            "model": self.config.name,
            "google_api_key": self.config.api_key,
            "temperature": self.config.temperature,
        }
        if self.config.max_tokens:
            kwargs["max_output_tokens"] = self.config.max_tokens
        return ChatGoogleGenerativeAI(**kwargs)

    def get_provider_name(self) -> str:
        return "Google Gemini"
