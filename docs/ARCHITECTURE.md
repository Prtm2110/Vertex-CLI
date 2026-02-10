# Architecture Documentation

## Overview

Vertex-CLI uses LangChain for unified LLM interactions with a clean, modular architecture following SOLID principles.

## Architecture Layers

```
CLI Layer (prompt.py, llm.py)
    |
    v
Service Layer (LLMService, ConfigurationManager)
    |
    v
Provider Layer (ILLMProvider implementations)
    |
    v
LangChain Layer (ChatGoogleGenerativeAI, ChatOpenAI, ChatAnthropic)
```

## Core Components

### 1. Base Interfaces

**ILLMProvider** (`cli/models/base.py`)
- Abstract interface for all LLM providers
- Methods: `generate()`, `get_provider_name()`, `validate_config()`

**BaseLLMProvider** (`cli/models/base_provider.py`)
- Base implementation with common functionality
- Implements DRY principle
- Provides: lazy initialization, validation, generation logic

### 2. Provider Implementations

All providers extend `BaseLLMProvider` and only implement:
- `_create_llm()`: Provider-specific LLM instantiation
- `get_provider_name()`: Return provider name

**Providers:**
- `GeminiProvider`: Google Gemini integration
- `OpenAIProvider`: OpenAI GPT integration
- `AnthropicProvider`: Anthropic Claude integration

### 3. Factory Pattern

**LLMProviderFactory** (`cli/models/factory.py`)
- Creates provider instances based on configuration
- Supports provider registration for extensibility
- Auto-detects provider from model name

### 4. Service Layer

**ConfigurationManager** (`cli/config_manager.py`)
- Manages model configurations
- Storage: `~/.config/ai_model_manager/models_config.json`
- Operations: CRUD for models, selection management

**LLMService** (`cli/llm_service.py`)
- Orchestrates LLM interactions
- Provider caching for performance
- Dependency injection pattern

## SOLID Principles

### Single Responsibility
Each class has one clear purpose:
- `ConfigurationManager`: Configuration persistence
- `LLMService`: LLM orchestration
- Provider classes: Provider-specific logic

### Open/Closed
- Easy to add new providers without modifying existing code
- Factory pattern enables extension

### Liskov Substitution
- All providers implement `ILLMProvider`
- Providers are interchangeable

### Interface Segregation
- `ILLMProvider` defines only essential operations
- Clean, focused contracts

### Dependency Inversion
- High-level modules depend on abstractions
- Dependency injection throughout

## Configuration Format

```json
{
  "selected_model": "gpt-4",
  "models": {
    "gemini-2.5-flash": {
      "provider": "google",
      "api_key": "your-api-key",
      "temperature": 0.7,
      "max_tokens": null
    }
  }
}
```

## Adding New Providers

1. Create provider class extending `BaseLLMProvider`
2. Implement `_create_llm()` and `get_provider_name()`
3. Register in `LLMProviderFactory`

Example:
```python
from cli.models.base_provider import BaseLLMProvider

class YourProvider(BaseLLMProvider):
    def _create_llm(self):
        return ChatYourProvider(
            model=self.config.name,
            api_key=self.config.api_key,
            temperature=self.config.temperature
        )

    def get_provider_name(self):
        return "Your Provider"
```

## Testing

Comprehensive test suite: `tests/test_vertex.py`

Run tests:
```bash
python tests/test_vertex.py
```
