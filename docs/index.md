# Homepage

### Install Vertex-CLI from TestPyPI

Vertex-CLI is a command-line tool that lets you use LLMs to answer queries and debug faster.
For example, you can run:

```bash
tex "tell me about the solar system"
```

![Example usage](images/eg_matplotlib.gif)

Replace `"tell me about the solar system"` with any query you like, and Vertex-CLI will generate an accurate response.

### Installation

To install [`Vertex-CLI`](https://github.com/prtm2110/vertex-cli) from TestPyPI, use:

```bash
pip install -i https://test.pypi.org/simple/ Vertex-CLI
tex-init
```
Or install Vertex-CLI in editable mode. See the [Contributors Guide](contributors_guide.md) for details.

### Managing API Keys

- **Add a model and its API key:**
  ```bash
  tex --config <model-name> <api-key>
  ```
- **Remove a model:**
  ```bash
  tex --remove <model-name>
  ```
- **Select a model:**
  ```bash
  tex --select
  ```

### Documentation

- Full CLI tool docs: [CLI Tool Docs](cli_tool_docs.md)
- Contribution guide: [Contributors Guide](contributors_guide.md)
- API reference: [API Reference](references.md)

---
