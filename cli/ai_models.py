"""
AI Models Management Module

This module handles the configuration and interaction with various AI models,
primarily focusing on Google's Generative AI integration. It manages API keys,
model configurations, and generation of AI responses.
"""

import json
import os
import threading
from cli.utils import spin_loader

FILE_NAME = os.path.join(os.path.dirname(__file__), "..", "models_api.json")


def load_models_api():
    """
    Load API configurations from JSON file.

    Returns:
        dict: Dictionary containing model names and their API keys.
              Returns None if file not found.

    Example:
        >>> load_models_api()
        {'gemini-1.5-flash': 'api_key_123', 'gpt-4': 'api_key_456'}
    """
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        pass


def update_models_api_json(updated_json_data):
    """
    Update the models API configuration JSON file.

    Args:
        updated_json_data (dict): Updated configuration data to be written to file.

    """
    with open(FILE_NAME, "w") as f:
        json.dump(updated_json_data, f, indent=4)


def api_key_model_selection(model_name):
    """
    Retrieve API key for specified model.

    Args:
        model_name (str): Name of the AI model.

    Returns:
        str: API key associated with the model.

    Raises:
        ValueError: If model is not found or has no API key.

    Example:
        >>> api_key_model_selection('gemini-1.5-flash')
        'your_api_key_here'
    """
    models_api_dict = load_models_api()
    if model_name in models_api_dict and models_api_dict[model_name]:
        return models_api_dict[model_name]
    else:
        raise ValueError(
            f"Model '{model_name}' is not available or has no API key. Please add it."
        )


def remove_model(model_name):
    """
    Remove a model from the configuration.

    Args:
        model_name (str): Name of the model to remove.

    Raises:
        ValueError: If model is not found in configuration.

    Example:
        >>> remove_model('gemini-1.5-flash')
        "Model 'gemini-1.5-flash' removed successfully."
    """
    models_api_dict = load_models_api()
    if model_name in models_api_dict:
        del models_api_dict[model_name]
        update_models_api_json(models_api_dict)
        print(f"Model '{model_name}' removed successfully.")
    else:
        raise ValueError(f"Model '{model_name}' is not found.")


def create_json_file():
    """
    Create a JSON file with the specified default configuration.

    Args:
        FILE_NAME (str): The name of the file to be created.
        default_config (dict): The default configuration to write to the file.
    """
    # A testing api key for gemini-1.5-flash is added.
    default_config = {
        "selected_model": None,
        "gemini-1.5-flash": "AIzaSyCSXtRAITXfGuarMHI1j-0QyKkoT9mUfz8",
        "gemini-1.5-interactive": None,
        "gemini-1.5-creative": None,
    }

    with open(FILE_NAME, "w") as f:
        json.dump(default_config, f, indent=4)
    print("JSON file created successfully.")


def configure_model(model_name, api_key):
    """
    Add or update a model's API key configuration.

    Args:
        model_name (str): Name of the model to configure.
        api_key (str): API key for the model.

    Example:
        >>> configure_model('gemini-1.5-flash', 'your_api_key_here')
        "Model added successfully."
    """
    models_api_dict = load_models_api()
    models_api_dict[model_name] = api_key
    update_models_api_json(models_api_dict)
    print("Model added successfully.")


def list_models():
    """
    List all available models and their API keys.

    Example:
        ``tex --list``
        gemini-1.5-flash: your_api_key_here
    """
    models_api_dict = load_models_api()
    if models_api_dict:
        for model, api_key in models_api_dict.items():
            print(f"{model}: {api_key}")
    else:
        print("No models found.")


def select_model(model_name):
    models_api_dict = load_models_api()

    if model_name in models_api_dict and models_api_dict[model_name]:
        models_api_dict["selected_model"] = model_name
        update_models_api_json(models_api_dict)
        print(f"Selected model: {model_name}")
    else:
        print("No models found or there is no api key for that model")


def generate_output(model_name, prompt_by_user):
    """
    Generate AI response using specified model.

    Args:
        model_name (str): Name of the AI model to use.
        prompt_by_user (str): User's input prompt.

    Returns:
        str: Generated response text.
    """
    from cli.llm import gemini_api_output

    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spin_loader, args=(stop_spinner,))
    spinner_thread.start()
    #############################

    output = gemini_api_output(model_name, prompt_by_user)

    #############################
    stop_spinner.set()
    spinner_thread.join()

    return output
