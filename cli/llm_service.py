"""Service for LLM generation and orchestration."""

import threading
from typing import Optional
from cli.config_manager import ConfigurationManager
from cli.models.base import ILLMProvider, ModelConfig
from cli.models.factory import LLMProviderFactory
from cli.utils import spin_loader


class LLMService:
    """Service for generating LLM responses."""

    def __init__(self, config_manager: Optional[ConfigurationManager] = None):
        """
        Initialize LLM service.

        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager or ConfigurationManager()
        self._provider_cache: dict[str, ILLMProvider] = {}

    def _get_provider(self, model_name: str) -> ILLMProvider:
        """Get or create a provider instance for the model."""
        if model_name in self._provider_cache:
            return self._provider_cache[model_name]

        # Get model configuration
        model_config_dict = self.config_manager.get_model_config(model_name)
        if not model_config_dict:
            raise ValueError(f"Model '{model_name}' is not configured.")

        if not model_config_dict.get("api_key"):
            raise ValueError(f"Model '{model_name}' has no API key configured.")

        # Create ModelConfig object
        model_config = ModelConfig(
            name=model_name,
            provider=model_config_dict["provider"],
            api_key=model_config_dict["api_key"],
            temperature=model_config_dict.get("temperature", 0.7),
            max_tokens=model_config_dict.get("max_tokens"),
        )

        # Create provider using factory
        provider = LLMProviderFactory.create(model_config)

        # Cache the provider
        self._provider_cache[model_name] = provider

        return provider

    def generate(
        self,
        prompt: str,
        model_name: Optional[str] = None,
        show_spinner: bool = True,
        **kwargs,
    ) -> str:
        """Generate response from LLM."""
        if model_name is None:
            model_name = self.config_manager.get_selected_model()
            if not model_name:
                # Fall back to default
                model_name = "gemini-2.5-flash"

        # Get provider
        provider = self._get_provider(model_name)

        # Generate with optional spinner
        if show_spinner:
            stop_spinner = threading.Event()
            spinner_thread = threading.Thread(target=spin_loader, args=(stop_spinner,))
            spinner_thread.start()

            try:
                response = provider.generate(prompt, **kwargs)
            finally:
                stop_spinner.set()
                spinner_thread.join()
        else:
            response = provider.generate(prompt, **kwargs)

        return response
