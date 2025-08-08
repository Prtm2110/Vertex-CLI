# Vertex CLI

Vertex CLI is a powerful command-line tool that leverages multiple Large Language Models (LLMs) to answer queries and debug faster. With support for OpenAI GPT models, Anthropic Claude, and Google Gemini, you can choose the best model for your needs.

**Complete Documentation:** [Vertex CLI Docs](https://prtm2110.github.io/Vertex-CLI/)


---

## Installation and Setup

Follow these steps to get started:

### Install Vertex-CLI from TestPyPI

To install [`Vertex-CLI`](https://github.com/prtm2110/vertex-cli) from TestPyPI, run:

```bash
pip install -i https://test.pypi.org/simple/ Vertex-CLI
```

After installation, initialize the CLI configuration file:

```bash
tex-init
```

This will create the `models_api.json` under `~/.config/ai_model_manager/` with default entries.

---

### Install the Editable Version (For Development)

If you want to modify or contribute to Vertex CLI, install it in **editable mode**:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Prtm2110/Vertex-CLI
   cd Vertex-CLI
   ```

2. **Install dependencies and set up the project:**

   ```bash
   pip install -e .
   ```

3. **Initialize the CLI:**

   ```bash
   tex-init
   ```

---

## 🚀 Supported Models

Vertex CLI supports models from multiple providers:

### 🤖 OpenAI Models
- `gpt-4o` - Latest GPT-4 Omni model  
- `gpt-4o-mini` - Faster, cost-effective GPT-4 Omni
- `gpt-4-turbo` - GPT-4 Turbo with improved performance
- `gpt-4` - Original GPT-4 model
- `gpt-3.5-turbo` - Fast and efficient model
- `chatgpt` - Alias for gpt-3.5-turbo

### 🧠 Anthropic Claude Models  
- `claude-3-5-sonnet` - Latest Claude 3.5 Sonnet
- `claude-3-5-haiku` - Fast Claude 3.5 Haiku
- `claude-3-opus` - Most capable Claude 3 model
- `claude-3-sonnet` - Balanced Claude 3 model
- `claude-3-haiku` - Fast Claude 3 model

### 🔮 Google Gemini Models
- `gemini-1.5-pro` - Advanced Gemini model
- `gemini-1.5-flash` - Fast Gemini model  
- `gemini-1.5-flash-8b` - Efficient 8B parameter model
- `gemini-pro` - Standard Gemini model

---

## ⚙️ Configuration

### View All Supported Models
```bash
tex models
```

### Configure API Keys

Configure your API keys for different providers:

```bash
# OpenAI
tex config gpt-4o YOUR_OPENAI_API_KEY
tex config gpt-3.5-turbo YOUR_OPENAI_API_KEY

### Model Management

List configured models and their status:
```bash
tex list
```

Select a default model:
```bash
tex select gpt-4o
# or
tex select claude-3-5-sonnet  
# or
tex select gemini-1.5-pro
```

Remove a model configuration:
```bash
tex remove model-name
```

---

## Usage

Once installed and configured, you can start chatting or debugging commands:

### Chat with the LLM

You can either use the `chat` subcommand or omit it entirely:

```bash
# Explicit subcommand
tex chat "Tell me about the solar system"

# Shortcut form (no subcommand)
tex "Tell me about the solar system"
```

Replace the quoted string with any query you'd like.

![alt text](docs/images/eg_matplotlib.gif)

🔗 **Complete CLI Documentation:** [CLI Commands](https://prtm2110.github.io/Vertex-CLI/cli_tool_docs/)

---

## Debugging Mode (Beta Feature)

Debugging is currently in beta but can analyze recent shell commands to identify issues.

### Debug the Last 3 Commands (default)

```bash
tex debug
```

### Specify the Number of Commands to Debug

```bash
tex debug -n 5
```

### Add a Custom Debugging Message

```bash
tex debug -n 5 -p "Explain why \`git commit\` failed"
```

---

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. **Fork the repository**
2. **Create a new branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes**:

   ```bash
   git commit -m "Add your feature description"
   ```
4. **Push your branch**:

   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a pull request**

🔗 **Contributor Guide:** [How to Contribute](https://prtm2110.github.io/Vertex-CLI/contributors_guide/)

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Prtm2110/Vertex-CLI/blob/main/LICENSE) file for more details.

---

## Support

If you encounter any issues, open an issue on the **[GitHub repository](https://github.com/Prtm2110/Vertex-CLI/issues)**.
