"""
Simple smoke tests to verify the CI/CD setup works.
These tests don't require any external dependencies or API keys.
"""

import os
import sys
import tempfile
import json

# Add cli to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_imports():
    """Test that all modules can be imported."""
    from cli.chat_history import ChatHistory
    from cli.config_manager import ConfigurationManager
    from cli.models.base import ModelConfig
    from cli.models.factory import LLMProviderFactory

    assert ChatHistory is not None
    assert ConfigurationManager is not None
    assert ModelConfig is not None
    assert LLMProviderFactory is not None


def test_model_config_basic():
    """Test basic ModelConfig creation."""
    from cli.models.base import ModelConfig

    config = ModelConfig(name="test-model", provider="google", api_key="test-key", temperature=0.7)
    assert config.name == "test-model"
    assert config.provider == "google"
    assert config.api_key == "test-key"
    assert config.temperature == 0.7


def test_configuration_manager_basic():
    """Test basic ConfigurationManager operations."""
    from cli.config_manager import ConfigurationManager

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_file = f.name

    try:
        manager = ConfigurationManager(temp_file)
        assert os.path.exists(temp_file)

        # Test setting config
        manager.set_model_config("test-model", "google", "test-key", 0.8)

        # Test getting config
        config = manager.get_model_config("test-model")
        assert config is not None
        assert config["provider"] == "google"

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_chat_history_basic():
    """Test basic ChatHistory operations."""
    from cli.chat_history import ChatHistory

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_file = f.name

    try:
        history = ChatHistory(temp_file, max_length=5)

        # Test appending
        history.append("user", "Hello")
        assert len(history.history) == 1

        # Test getting prompt
        prompt = history.get_prompt()
        assert "Hello" in prompt

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_provider_factory():
    """Test provider factory creates correct providers."""
    from cli.models.base import ModelConfig
    from cli.models.factory import LLMProviderFactory

    # Test Gemini
    config = ModelConfig("gemini-2.5-flash", "google", "test-key", 0.7)
    provider = LLMProviderFactory.create(config)
    assert provider.__class__.__name__ == "GeminiProvider"

    # Test OpenAI
    config = ModelConfig("gpt-4", "openai", "test-key", 0.7)
    provider = LLMProviderFactory.create(config)
    assert provider.__class__.__name__ == "OpenAIProvider"

    # Test Anthropic
    config = ModelConfig("claude-3-opus", "anthropic", "test-key", 0.7)
    provider = LLMProviderFactory.create(config)
    assert provider.__class__.__name__ == "AnthropicProvider"


if __name__ == "__main__":
    print("Running smoke tests...")
    test_imports()
    print("✓ Imports work")

    test_model_config_basic()
    print("✓ ModelConfig works")

    test_configuration_manager_basic()
    print("✓ ConfigurationManager works")

    test_chat_history_basic()
    print("✓ ChatHistory works")

    test_provider_factory()
    print("✓ Provider factory works")

    print("\nAll smoke tests passed! ✓")
