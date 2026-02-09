"""Configuration manager for AI models."""

import json
import os
from typing import Optional, Dict, Any


class ConfigurationManager:
    """Manages model configurations stored in JSON."""

    def __init__(self, file_path: Optional[str] = None):
        if file_path is None:
            config_dir = os.path.join(os.path.expanduser("~"), ".config", "ai_model_manager")
            os.makedirs(config_dir, exist_ok=True)
            file_path = os.path.join(config_dir, "models_config.json")

        self.file_path = file_path

        if not os.path.exists(self.file_path):
            self._create_default_config()

    def _create_default_config(self) -> None:
        """Create default configuration file."""
        default_config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config", "default_config.json"
        )

        try:
            with open(default_config_path, "r") as f:
                default_config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Fallback if JSON file not found
            default_config = {"selected_model": None, "models": {}}

        self._write_config(default_config)
        print(f"Configuration file created at: {self.file_path}")

    def _read_config(self) -> Dict[str, Any]:
        """Read configuration from file."""
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"selected_model": None, "models": {}}

    def _write_config(self, data: Dict[str, Any]) -> None:
        """Write configuration to file."""
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def get_model_config(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific model."""
        config = self._read_config()
        return config.get("models", {}).get(model_name)

    def set_model_config(
        self,
        model_name: str,
        provider: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> None:
        """Set or update configuration for a model."""
        config = self._read_config()

        if "models" not in config:
            config["models"] = {}

        config["models"][model_name] = {
            "provider": provider,
            "api_key": api_key,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        self._write_config(config)
        print(f"Model '{model_name}' configured successfully.")

    def remove_model(self, model_name: str) -> None:
        """Remove a model from configuration."""
        config = self._read_config()

        if model_name not in config.get("models", {}):
            raise ValueError(f"Model '{model_name}' not found in configuration.")

        del config["models"][model_name]

        # Clear selected model if it was the removed one
        if config.get("selected_model") == model_name:
            config["selected_model"] = None

        self._write_config(config)
        print(f"Model '{model_name}' removed successfully.")

    def get_selected_model(self) -> Optional[str]:
        """Get the currently selected model name."""
        config = self._read_config()
        return config.get("selected_model")

    def set_selected_model(self, model_name: str) -> None:
        """Set the active model."""
        config = self._read_config()
        model_config = config.get("models", {}).get(model_name)

        if not model_config:
            raise ValueError(f"Model '{model_name}' is not configured.")

        if not model_config.get("api_key"):
            raise ValueError(f"Model '{model_name}' has no API key configured.")

        config["selected_model"] = model_name
        self._write_config(config)
        print(f"Selected model: {model_name}")

    def list_models(self) -> Dict[str, Dict[str, Any]]:
        """Get all configured models."""
        config = self._read_config()
        return config.get("models", {})
