"""
Simplified LLM Provider system with automatic dependency installation.
Supports OpenAI GPT models, Anthropic Claude, and Google Gemini.
"""

import os
import subprocess
import sys
from typing import Dict, Optional


def install_package(package_name: str) -> bool:
    """Install a Python package using pip."""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def ensure_dependencies(provider: str) -> bool:
    """Ensure required dependencies are installed for a provider."""
    dependencies = {"openai": ["openai>=1.0.0"], "anthropic": ["anthropic>=0.30.0"], "google": ["google-generativeai>=0.8.0"]}

    if provider not in dependencies:
        return False

    for package in dependencies[provider]:
        try:
            __import__(package.split(">=")[0].replace("-", "_"))
        except ImportError:
            print(f"Installing {package}...")
            if not install_package(package):
                print(f"Failed to install {package}")
                return False

    return True


class LLMProvider:
    """Base LLM provider class."""

    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key

    def generate_response(self, prompt: str, system_instruction: str = None) -> str:
        """Generate a response using the LLM."""
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    def generate_response(self, prompt: str, system_instruction: str = None) -> str:
        if not ensure_dependencies("openai"):
            raise Exception("Failed to install OpenAI dependencies")

        try:
            import openai

            client = openai.OpenAI(api_key=self.api_key)

            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(model=self.model_name, messages=messages, temperature=0.7)
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "invalid_api_key" in error_msg:
                raise Exception(
                    f"❌ Invalid OpenAI API key. Get your key at: https://platform.openai.com/api-keys\n   Run: tex config {self.model_name} YOUR_ACTUAL_API_KEY"
                )
            elif "quota" in error_msg.lower() or "billing" in error_msg.lower():
                raise Exception(
                    f"❌ OpenAI quota exceeded or billing issue. Check your account at: https://platform.openai.com/account/billing"
                )
            else:
                raise Exception(f"OpenAI API error: {str(e)}")


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""

    def generate_response(self, prompt: str, system_instruction: str = None) -> str:
        if not ensure_dependencies("anthropic"):
            raise Exception("Failed to install Anthropic dependencies")

        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            messages = [{"role": "user", "content": prompt}]

            kwargs = {"model": self.model_name, "max_tokens": 1000, "messages": messages}

            if system_instruction:
                kwargs["system"] = system_instruction

            response = client.messages.create(**kwargs)
            return response.content[0].text
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "invalid" in error_msg.lower():
                raise Exception(
                    f"❌ Invalid Anthropic API key. Get your key at: https://console.anthropic.com/\n   Run: tex config {self.model_name} YOUR_ACTUAL_API_KEY"
                )
            elif "quota" in error_msg.lower() or "billing" in error_msg.lower():
                raise Exception(
                    f"❌ Anthropic quota exceeded or billing issue. Check your account at: https://console.anthropic.com/settings/billing"
                )
            else:
                raise Exception(f"Anthropic API error: {str(e)}")


class GoogleProvider(LLMProvider):
    """Google Gemini provider."""

    def generate_response(self, prompt: str, system_instruction: str = None) -> str:
        if not ensure_dependencies("google"):
            raise Exception("Failed to install Google dependencies")

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)

            full_prompt = prompt
            if system_instruction:
                full_prompt = f"{system_instruction}\n\n{prompt}"

            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "invalid" in error_msg.lower() or "API_KEY_INVALID" in error_msg:
                raise Exception(
                    f"❌ Invalid Google API key. Get your key at: https://makersuite.google.com/app/apikey\n   Run: tex config {self.model_name} YOUR_ACTUAL_API_KEY"
                )
            elif "quota" in error_msg.lower() or "billing" in error_msg.lower():
                raise Exception(
                    f"❌ Google API quota exceeded. Check your quota at: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas"
                )
            else:
                raise Exception(f"Google API error: {str(e)}")


class LLMProviderFactory:
    """Factory for creating LLM providers."""

    # Model mappings
    MODELS = {
        # OpenAI models
        "gpt-4o": ("openai", "gpt-4o"),
        "gpt-4o-mini": ("openai", "gpt-4o-mini"),
        "gpt-4-turbo": ("openai", "gpt-4-turbo"),
        "gpt-4": ("openai", "gpt-4"),
        "gpt-3.5-turbo": ("openai", "gpt-3.5-turbo"),
        "chatgpt": ("openai", "gpt-3.5-turbo"),
        # Anthropic models
        "claude-3-5-sonnet": ("anthropic", "claude-3-5-sonnet-20241022"),
        "claude-3-5-haiku": ("anthropic", "claude-3-5-haiku-20241022"),
        "claude-3-opus": ("anthropic", "claude-3-opus-20240229"),
        "claude-3-sonnet": ("anthropic", "claude-3-sonnet-20240229"),
        "claude-3-haiku": ("anthropic", "claude-3-haiku-20240307"),
        # Google models
        "gemini-1.5-pro": ("google", "gemini-1.5-pro"),
        "gemini-1.5-flash": ("google", "gemini-1.5-flash"),
        "gemini-1.5-flash-8b": ("google", "gemini-1.5-flash-8b"),
        "gemini-pro": ("google", "gemini-pro"),
        # Backward compatibility
        "gemini-1.5-interactive": ("google", "gemini-1.5-pro"),
        "gemini-1.5-creative": ("google", "gemini-1.5-pro"),
    }

    @classmethod
    def create_provider(cls, model_name: str, api_key: str) -> LLMProvider:
        """Create an appropriate LLM provider based on the model name."""
        if model_name not in cls.MODELS:
            raise ValueError(f"Unsupported model: {model_name}")

        provider_type, actual_model = cls.MODELS[model_name]

        if provider_type == "openai":
            return OpenAIProvider(actual_model, api_key)
        elif provider_type == "anthropic":
            return AnthropicProvider(actual_model, api_key)
        elif provider_type == "google":
            return GoogleProvider(actual_model, api_key)
        else:
            raise ValueError(f"Unknown provider: {provider_type}")

    @classmethod
    def get_supported_models(cls) -> Dict[str, list]:
        """Get all supported models grouped by provider."""
        result = {"openai": [], "anthropic": [], "google": []}
        for model, (provider, _) in cls.MODELS.items():
            if model not in result[provider]:
                result[provider].append(model)
        return result

    @classmethod
    def get_provider_for_model(cls, model_name: str) -> str:
        """Get the provider name for a given model."""
        if model_name in cls.MODELS:
            return cls.MODELS[model_name][0]
        return "unknown"

    @classmethod
    def is_model_supported(cls, model_name: str) -> bool:
        """Check if a model is supported."""
        return model_name in cls.MODELS
