"""
Pytest configuration and shared fixtures.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add cli module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(scope="session")
def test_data_dir():
    """Provide test data directory path."""
    return Path(__file__).parent / "data"


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture(autouse=True)
def clean_environment():
    """Clean environment variables before each test."""
    # Store original env vars
    original_env = os.environ.copy()

    # Remove API keys from environment if they exist
    api_key_vars = [
        "GOOGLE_API_KEY",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "LANGCHAIN_API_KEY",
    ]

    for var in api_key_vars:
        os.environ.pop(var, None)

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests without external dependencies")
    config.addinivalue_line(
        "markers", "integration: Integration tests that may need external services"
    )
    config.addinivalue_line("markers", "slow: Tests that take longer to execute")
