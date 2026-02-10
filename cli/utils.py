import itertools
import sys
import time
import subprocess
from rich.console import Console
from rich.markdown import Markdown


def spin_loader(stop_event):
    """Display a spinning loader."""
    spinner = itertools.cycle(["-", "/", "|", "\\"])
    while not stop_event.is_set():
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")
    sys.stdout.write(" ")
    sys.stdout.flush()


def install_requirements():
    """Install required dependencies."""
    dependencies = [
        "rich>=14.0.0",
        "langchain>=0.1.0",
        "langchain-google-genai>=1.0.0",
        "langchain-openai>=0.0.5",
        "langchain-anthropic>=0.1.0",
    ]
    for package in dependencies:
        subprocess.run([sys.executable, "-m", "pip", "install", package])


def prettify_llm_output(response):
    """Prettify LLM output using Rich markdown."""
    console = Console()
    md = Markdown(response.strip())
    console.print("\n", md, "\n")
