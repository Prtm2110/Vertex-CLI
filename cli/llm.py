import os

from google import genai
from cli.ai_model_manager import AIModelManager
from cli.prettify_llm_output import prettify_llm_output
from cli.chat_history import ChatHistory


def gemini_api_output(model_name, prompt_by_user):
    """
    Generate AI response using specified model.

    Args:
        model_name (str): Name of the AI model to use.
        prompt_by_user (str): User's input prompt.

    Returns:
        str: Generated response text.
    """
    from cli.ai_model_manager import AIModelManager

    manager = AIModelManager()
    api_key = manager.get_api_key(model_name)

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=model_name, contents=prompt_by_user)

    return response.text


def generate_response(prompt: str, manager: AIModelManager, history: ChatHistory):
    system_instruction = (
        "System prompt: Give response in short and MD format, "
        "if asked for commands then give commands and don't explain too much"
    )
    full_prompt = f"{prompt}\n{system_instruction}"
    history.append("user", full_prompt)
    flat_prompt = history.get_prompt()
    models = manager.load()
    selected = models.get("selected_model")
    if not selected:
        selected = "gemini-1.5-flash"
    response = manager.generate_output(selected, flat_prompt)
    history.append("assistant", response or "")
    prettify_llm_output(response)
