import re
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax


def prettify_llm_output(response):
    """
    Prettifies the output from a language model response by processing it
    as Markdown with enhanced code block detection and syntax highlighting.

    Args:
        response (str): The raw response from the language model.

    Returns:
        None
    """
    console = Console()

    # Clean up the response
    markdown_output = response.strip()

    # Check if the entire response is just code without markdown formatting
    if _is_likely_code(markdown_output) and not _has_markdown_elements(markdown_output):
        # Treat the entire response as Python code
        syntax = Syntax(markdown_output, "python", theme="monokai", line_numbers=False)
        print()
        console.print(syntax)
        print()
        return

    # Check for code blocks and ensure they have language specification
    markdown_output = _enhance_code_blocks(markdown_output)

    # Render as markdown
    md = Markdown(markdown_output)
    print()
    console.print(md)
    print()


def _is_likely_code(text):
    """Check if text looks like Python code."""
    python_keywords = [
        "import",
        "def",
        "class",
        "if",
        "for",
        "while",
        "try",
        "except",
        "plt.",
    ]
    lines = text.split("\n")
    code_indicators = 0

    for line in lines:
        line = line.strip()
        if any(keyword in line for keyword in python_keywords):
            code_indicators += 1
        if line.startswith("#"):  # Comments
            code_indicators += 1

    return code_indicators >= 2 or any(
        keyword in text for keyword in ["plt.", "matplotlib", "import"]
    )


def _has_markdown_elements(text):
    """Check if text contains markdown elements."""
    markdown_indicators = ["#", "**", "*", "`", ">", "-", "1.", "[", "]"]
    return any(indicator in text for indicator in markdown_indicators)


def _enhance_code_blocks(text):
    """Add language specification to code blocks that don't have it."""
    # Pattern to find code blocks without language specification
    pattern = r"```\n(.*?)\n```"

    def replace_code_block(match):
        code_content = match.group(1)
        if _is_likely_code(code_content):
            return f"```python\n{code_content}\n```"
        return match.group(0)

    # Replace code blocks without language specification
    enhanced = re.sub(pattern, replace_code_block, text, flags=re.DOTALL)

    return enhanced
