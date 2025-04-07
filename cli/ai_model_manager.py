import json
import os
import threading
from cli.utils import spin_loader
from cli.llm import gemini_api_output


class AIModelManager:
    """
    A class to manage AI model configurations stored in a JSON file.
    """

    def __init__(self, file_path=None):
        """
        Initialize the manager. Defaults to ~/.config/ai_model_manager/models_api.json
        """
        if file_path is None:
            config_dir = os.path.join(
                os.path.expanduser("~"), ".config", "ai_model_manager"
            )
            os.makedirs(config_dir, exist_ok=True)
            file_path = os.path.join(config_dir, "models_api.json")

        self.file_path = file_path

        if not os.path.exists(self.file_path):
            self.create_default_file()

    def _read_json(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _write_json(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def create_default_file(self):
        """
        Create a JSON file with a default model configuration.
        """
        default_config = {
            "selected_model": None,
            "gemini-1.5-flash": "AIzaSyCSXtRAITXfGuarMHI1j-0QyKkoT9mUfz8",
            "gemini-1.5-interactive": None,
            "gemini-1.5-creative": None,
        }
        self._write_json(default_config)
        print(f"Config file created at: {self.file_path}")

    def load(self):
        return self._read_json()

    def configure_model(self, model_name, api_key):
        data = self._read_json()
        data[model_name] = api_key
        self._write_json(data)
        print("Model added successfully.")

    def remove_model(self, model_name):
        data = self._read_json()
        if model_name in data:
            del data[model_name]
            self._write_json(data)
            print(f"Model '{model_name}' removed successfully.")
        else:
            raise ValueError(f"Model '{model_name}' not found.")

    def get_api_key(self, model_name):
        data = self._read_json()
        if model_name in data and data[model_name]:
            return data[model_name]
        raise ValueError(f"Model '{model_name}' is not available or has no API key.")

    def list_models(self):
        data = self._read_json()
        if data:
            for model, key in data.items():
                print(f"{model}: {key}")
        else:
            print("No models found.")

    def select_model(self, model_name):
        data = self._read_json()
        if model_name in data and data[model_name]:
            data["selected_model"] = model_name
            self._write_json(data)
            print(f"Selected model: {model_name}")
        else:
            print("No models found or no API key for that model.")

    def generate_output(self, model_name, prompt_by_user):
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(target=spin_loader, args=(stop_spinner,))
        spinner_thread.start()

        output = gemini_api_output(model_name, prompt_by_user)

        stop_spinner.set()
        spinner_thread.join()

        return output
