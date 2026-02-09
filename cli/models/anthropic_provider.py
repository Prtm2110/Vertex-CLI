"""Anthropic Claude provider implementation using LangChain."""

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from cli.models.base_provider import BaseLLMProvider


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude LLM provider."""

    def _create_llm(self) -> BaseChatModel:
        kwargs = {
            "model": self.config.name,
            "anthropic_api_key": self.config.api_key,
            "temperature": self.config.temperature,
        }
        if self.config.max_tokens:
            kwargs["max_tokens"] = self.config.max_tokens
        return ChatAnthropic(**kwargs)

    def get_provider_name(self) -> str:
        return "Anthropic Claude"
