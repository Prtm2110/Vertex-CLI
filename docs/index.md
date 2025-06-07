## Homepage

### Install Vertex-CLI from TestPyPI

**Vertex-CLI** is a command-line tool that lets you query Large Language Models (LLMs) and debug faster, straight from your terminal.

For example, you can run:

```bash
tex "tell me about the solar system"
```

![Example usage](images/eg_matplotlib.gif)

Replace `"tell me about the solar system"` with any query you like Vertex-CLI will generate a response using your selected LLM model.

---

### Installation

To install [`Vertex-CLI`](https://github.com/prtm2110/vertex-cli) from **TestPyPI**, run:

```bash
pip install -i https://test.pypi.org/simple/ Vertex-CLI
```

Then initialize the CLI with:

```bash
tex --setup
```

---

###  Managing API Keys & Models

* **Add a model and its API key:**

  ```bash
  tex config <model-name> <api-key>
  ```

* **Remove a model:**

  ```bash
  tex remove <model-name>
  ```

* **List all configured models:**

  ```bash
  tex list
  ```

* **Select a model to use by default:**

  ```bash
  tex select <model-name>
  ```

---

### Documentation

* Full CLI tool docs: [CLI Tool Docs](cli_tool_docs.md)
* Contributor guide: [Contributors Guide](contributors_guide.md)
* API reference: [API Reference](references.md)
