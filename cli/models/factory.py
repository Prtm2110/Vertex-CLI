"""Factory for creating LLM provider instances."""

from typing import Dict, Type
from cli.models.base import ILLMProvider, ModelConfig
from cli.models.gemini_provider import GeminiProvider
from cli.models.openai_provider import OpenAIProvider
from cli.models.anthropic_provider import AnthropicProvider


class LLMProviderFactory:
    """Factory for creating LLM provider instances."""

    _providers: Dict[str, Type[ILLMProvider]] = {
        "google": GeminiProvider,
        "gemini": GeminiProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "claude": AnthropicProvider,
    }

    _model_patterns = {
        "gemini": "google",
        "gpt": "openai",
        "claude": "anthropic",
    }

    @classmethod
    def create(cls, config: ModelConfig) -> ILLMProvider:
        """Create an LLM provider instance based on configuration."""
        provider_key = config.provider.lower()

        if provider_key in cls._providers:
            return cls._providers[provider_key](config)

        inferred_provider = cls._infer_provider_from_model(config.name)
        if inferred_provider:
            return cls._providers[inferred_provider](config)

        raise ValueError(
            f"Unsupported provider: {config.provider}. "
            f"Available: {', '.join(cls.get_supported_providers())}"
        )

    @classmethod
    def _infer_provider_from_model(cls, model_name: str) -> str | None:
        """Infer provider from model name."""
        model_lower = model_name.lower()
        for pattern, provider in cls._model_patterns.items():
            if pattern in model_lower:
                return provider
        return None

    @classmethod
    def get_supported_providers(cls) -> list[str]:
        """Get list of supported provider names."""
        return list(set(cls._providers.keys()))
