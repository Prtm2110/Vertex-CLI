"""
Test suite for Vertex-CLI refactored architecture.
Tests core functionality: models, providers, configuration, and services.
"""

import os
import sys
import tempfile
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cli.models.base import ModelConfig
from cli.models.factory import LLMProviderFactory
from cli.models.gemini_provider import GeminiProvider
from cli.models.openai_provider import OpenAIProvider
from cli.models.anthropic_provider import AnthropicProvider
from cli.config_manager import ConfigurationManager
from cli.llm_service import LLMService
from cli.chat_history import ChatHistory


def test_model_config():
    """Test ModelConfig dataclass."""
    config = ModelConfig(name="test-model", provider="google", api_key="test-key", temperature=0.5)
    assert config.name == "test-model"
    assert config.provider == "google"
    assert config.temperature == 0.5
    print("PASS: ModelConfig")


def test_provider_factory():
    """Test LLMProviderFactory."""
    # Test Gemini
    config = ModelConfig("gemini-2.5-flash", "google", "test-key", 0.7)
    provider = LLMProviderFactory.create(config)
    assert isinstance(provider, GeminiProvider)

    # Test OpenAI
    config = ModelConfig("gpt-4", "openai", "test-key", 0.7)
    provider = LLMProviderFactory.create(config)
    assert isinstance(provider, OpenAIProvider)

    # Test Anthropic
    config = ModelConfig("claude-3-opus", "anthropic", "test-key", 0.7)
    provider = LLMProviderFactory.create(config)
    assert isinstance(provider, AnthropicProvider)

    # Test auto-detection
    config = ModelConfig("gemini-pro", "unknown", "test-key", 0.7)
    provider = LLMProviderFactory.create(config)
    assert isinstance(provider, GeminiProvider)

    print("PASS: Provider Factory")


def test_configuration_manager():
    """Test ConfigurationManager."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_file = f.name

    try:
        manager = ConfigurationManager(temp_file)

        # Test adding model
        manager.set_model_config("test-model", "google", "test-key", 0.8)
        config = manager.get_model_config("test-model")
        assert config["provider"] == "google"
        assert config["temperature"] == 0.8

        # Test selecting model
        manager.set_selected_model("test-model")
        assert manager.get_selected_model() == "test-model"

        # Test listing
        models = manager.list_models()
        assert "test-model" in models

        # Test removing
        manager.remove_model("test-model")
        assert manager.get_model_config("test-model") is None

        print("PASS: Configuration Manager")

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_llm_service():
    """Test LLMService."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_file = f.name

    try:
        config_manager = ConfigurationManager(temp_file)
        config_manager.set_model_config("gemini-2.5-flash", "google", "test-key", 0.7)

        llm_service = LLMService(config_manager)

        # Test provider retrieval
        provider = llm_service._get_provider("gemini-2.5-flash")
        assert isinstance(provider, GeminiProvider)

        # Test caching
        provider2 = llm_service._get_provider("gemini-2.5-flash")
        assert provider is provider2

        print("PASS: LLM Service")

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_provider_validation():
    """Test provider validation."""
    try:
        config = ModelConfig("test", "google", "", 0.7)
        GeminiProvider(config)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    print("PASS: Provider Validation")


def test_chat_history():
    """Test ChatHistory functionality."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_file = f.name

    try:
        history = ChatHistory(temp_file, max_length=5)

        # Test appending messages
        history.append("user", "Hello")
        history.append("assistant", "Hi there")

        # Test prompt generation
        prompt = history.get_prompt()
        assert "User: Hello" in prompt
        assert "Assistant: Hi there" in prompt

        # Test max length
        for i in range(10):
            history.append("user", f"Message {i}")

        assert len(history.history) <= 5

        print("PASS: Chat History")

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_provider_auto_detection():
    """Test automatic provider detection from model names."""
    test_cases = [
        ("gemini-2.5-flash", GeminiProvider),
        ("gemini-pro", GeminiProvider),
        ("gpt-4", OpenAIProvider),
        ("gpt-3.5-turbo", OpenAIProvider),
        ("claude-3-opus", AnthropicProvider),
        ("claude-2", AnthropicProvider),
    ]

    for model_name, expected_provider in test_cases:
        config = ModelConfig(model_name, "unknown", "test-key", 0.7)
        provider = LLMProviderFactory.create(config)
        assert isinstance(
            provider, expected_provider
        ), f"Failed for {model_name}: expected {expected_provider}, got {type(provider)}"

    print("PASS: Provider Auto-Detection")


def test_configuration_persistence():
    """Test that configuration persists across manager instances."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_file = f.name

    try:
        # Create first manager and add config
        manager1 = ConfigurationManager(temp_file)
        manager1.set_model_config("persist-test", "google", "key123", 0.9)
        manager1.set_selected_model("persist-test")

        # Create second manager and verify persistence
        manager2 = ConfigurationManager(temp_file)
        config = manager2.get_model_config("persist-test")
        assert config is not None
        assert config["api_key"] == "key123"
        assert config["temperature"] == 0.9
        assert manager2.get_selected_model() == "persist-test"

        print("PASS: Configuration Persistence")

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_multiple_models_config():
    """Test managing multiple models simultaneously."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_file = f.name

    try:
        manager = ConfigurationManager(temp_file)

        # Configure multiple models
        models = [
            ("gemini-2.5-flash", "google", "key1"),
            ("gpt-4", "openai", "key2"),
            ("claude-3-opus", "anthropic", "key3"),
        ]

        for model_name, provider, api_key in models:
            manager.set_model_config(model_name, provider, api_key, 0.7)

        # Verify all models exist
        all_models = manager.list_models()
        assert len(all_models) >= 3

        for model_name, _, _ in models:
            assert model_name in all_models
            config = manager.get_model_config(model_name)
            assert config is not None
            assert config["api_key"] is not None

        print("PASS: Multiple Models Configuration")

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Vertex-CLI Test Suite")
    print("=" * 60 + "\n")

    tests = [
        test_model_config,
        test_provider_factory,
        test_configuration_manager,
        test_llm_service,
        test_provider_validation,
        test_chat_history,
        test_provider_auto_detection,
        test_configuration_persistence,
        test_multiple_models_config,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"FAIL: {test.__name__} - {e}")
            import traceback

            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
