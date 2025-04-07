from google import genai


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
