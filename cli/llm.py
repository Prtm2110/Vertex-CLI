"""LLM interaction module."""

from cli.llm_service import LLMService
from cli.utils import prettify_llm_output
from cli.chat_history import ChatHistory


def generate_response(prompt: str, llm_service: LLMService, history: ChatHistory):
    """Generate and display AI response."""
    system_instruction = (
        "System prompt: Give response in short and MD format, "
        "if asked for commands then give commands and don't explain too much"
    )

    full_prompt = f"{prompt}\n{system_instruction}"
    history.append("user", full_prompt)

    # Get conversation history as context
    flat_prompt = history.get_prompt()

    # Generate response using LLM service
    response = llm_service.generate(flat_prompt)

    # Save response to history
    history.append("assistant", response or "")

    # Display formatted output
    prettify_llm_output(response)
