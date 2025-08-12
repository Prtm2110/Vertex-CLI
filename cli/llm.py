import os
from cli.ai_model_manager import AIModelManager
from cli.prettify_llm_output import prettify_llm_output
from cli.chat_history import ChatHistory


def generate_response(prompt: str, manager: AIModelManager, history: ChatHistory):
    """Generate AI response using the selected model."""
    system_instruction = (
        "Give response in short and markdown format. " "If asked for commands, give commands without too much explanation."
    )

    # Add to history
    history.append("user", prompt)
    full_prompt = history.get_prompt()

    # Get selected model or use available one
    models = manager.load()
    selected = models.get("selected_model")

    if not selected:
        available = manager.get_available_models()
        if available:
            selected = available[0]
            print(f"ℹ️  Using {selected} (no model selected)")
        else:
            print("❌ No models configured! Configure one with:")
            print("   tex config MODEL_NAME YOUR_API_KEY")
            print("   tex models  # to see available models")
            return

    try:
        response = manager.generate_output(selected, full_prompt, system_instruction)
        history.append("assistant", response or "")
        prettify_llm_output(response)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if "not configured" in str(e).lower():
            print(f"💡 Configure {selected} with: tex config {selected} YOUR_API_KEY")
