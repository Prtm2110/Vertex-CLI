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

After installation, initialize the CLI:

```bash
tex-init
```

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

You can configure the CLI to use a specific LLM model:

```bash
tex --config gemini-1.5-flash <model-api-key>
```

Replace `gemini-1.5-flash` with your preferred model name and `<model-api-key>` with your API key.

---

## Usage

Once installed, you can start using Vertex CLI by running:

```bash
tex "tell me about the solar system"
```
![alt text](docs/images/eg_matplotlib.gif)

Replace `"tell me about solar system"` with any query you'd like.

🔗 **Complete CLI Documentation:** [CLI Commands](https://prtm2110.github.io/Vertex-CLI/cli_tool_docs/)

---

## Debugging Mode (Beta Feature)

Debugging is currently in beta but can analyze recent commands to identify issues.

### Debug the Last Two Commands

```bash
tex --debug
```

### Specify the Number of Commands to Debug

To debug the last 5 commands:

```bash
tex --debug --5
```

### Add a Custom Debugging Message

Provide additional context while debugging:

```bash
tex "I believe this can be solved by changing the environment variable" --debug
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
