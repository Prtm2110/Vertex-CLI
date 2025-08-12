# 🚀 Vertex CLI - Quick Start Guide

## Installation

```bash
git clone https://github.com/Prtm2110/vertex-cli.git
cd vertex-cli
pip install -e .
```

## Setup

```bash
# Create default configuration
python -m cli.prompt --setup

# See all supported models
python -m cli.prompt models
```

## Configure Models

```bash
# OpenAI
python -m cli.prompt config gpt-4o YOUR_OPENAI_API_KEY
python -m cli.prompt config gpt-3.5-turbo YOUR_OPENAI_API_KEY

# Anthropic
python -m cli.prompt config claude-3-5-sonnet YOUR_ANTHROPIC_API_KEY
python -m cli.prompt config claude-3-opus YOUR_ANTHROPIC_API_KEY

# Google (already has a demo key)
python -m cli.prompt config gemini-1.5-pro YOUR_GOOGLE_API_KEY
```

## Usage

```bash
# Select a model
python -m cli.prompt select gpt-4o

# Chat directly
python -m cli.prompt "Hello! How are you?"

# Use chat command
python -m cli.prompt chat "Explain quantum computing in simple terms"

# Debug bash commands
python -m cli.prompt debug

# List configured models
python -m cli.prompt list

# Remove a model
python -m cli.prompt remove model-name
```

## Features

✅ **Multi-Model Support**: OpenAI GPT, Anthropic Claude, Google Gemini
✅ **Automatic Dependencies**: Installs packages only when needed
✅ **Simple Configuration**: Easy API key management
✅ **Smart Defaults**: Uses available models intelligently
✅ **Rich Output**: Beautiful formatted responses
✅ **Chat History**: Maintains conversation context

## API Keys

- **OpenAI**: Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Anthropic**: Get your key from [Anthropic Console](https://console.anthropic.com/)
- **Google**: Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Example Session

```bash
$ python -m cli.prompt --setup
Config file created at: ~/.config/ai_model_manager/models_api.json

$ python -m cli.prompt config gpt-4o sk-your-key-here
✅ gpt-4o configured successfully.

$ python -m cli.prompt select gpt-4o
✅ Selected model: gpt-4o

$ python -m cli.prompt "What's the capital of France?"
Installing openai>=1.0.0...
The capital of France is **Paris**.
```

The CLI automatically installs dependencies when you first use a model provider!
