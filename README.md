# Vertex CLI

Vertex CLI is a powerful command-line tool that leverages Large Language Models (LLMs) to answer queries and debug faster. With just a few commands, you can set up and start using advanced features like querying LLMs and generating insights.

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

## Configuration

You can configure the CLI to use a specific LLM model by adding or updating your API key:

```bash
tex config gemini-1.5-flash YOUR_MODEL_API_KEY
```

Replace `gemini-1.5-flash` with your preferred model name and `YOUR_MODEL_API_KEY` with your API key.

To list all configured models:

```bash
tex list
```

To remove a model:

```bash
tex remove gemini-1.5-creative
```

To select a model as the default:

```bash
tex select gemini-1.5-flash
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
