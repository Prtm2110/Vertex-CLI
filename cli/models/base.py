"""Base interfaces and abstractions for LLM providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelConfig:
    """Configuration for an LLM model."""

    name: str
    provider: str
    api_key: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None


class ILLMProvider(ABC):
    """Interface for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of the provider."""
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the model configuration."""
        pass
