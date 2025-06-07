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
tex --setup
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

3. **Initialize the CLI configuration:**

   ```bash
   tex --setup
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

### Quick Command Reference

* **Convert an array to a NumPy array**

  ```bash
  tex "how to convert an array into a NumPy array"
  ```

* **Manage API keys for models**

  * Add or update a model’s API key:

    ```bash
    tex config <model-name> <api-key>
    ```
  * Remove a model:

    ```bash
    tex remove <model-name>
    ```
  * List all saved models and their API keys:

    ```bash
    tex list
    ```
  * Select a model to use:

    ```bash
    tex select <model-name>
    ```
  * Show available commands/help:

    ```bash
    tex -h
    tex chat -h
    ```

### Debugging (Beta Feature)

* Debug the last 3 commands (default):

  ```bash
  tex debug
  ```

* Debug a specific number of recent commands (e.g., last 5):

  ```bash
  tex debug -n 5
  ```

* Add a custom message to explain your assumptions or observations:

  ```bash
  tex debug -n 5 -p "I think this issue might be related to environment variables"
  ```

---

🔗 **Complete CLI Documentation:** [CLI Commands](https://prtm2110.github.io/Vertex-CLI/cli_tool_docs/)
