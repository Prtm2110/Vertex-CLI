import json
import os
import threading
from cli.utils import spin_loader
from cli.llm import gemini_api_output


class AIModelManager:
    """
    A class to manage AI model configurations stored in a JSON file.
    Allows adding, removing, selecting models, and generating output via LLM APIs.
    """

    def __init__(self, file_path=None):
        """
        Initialize the AIModelManager instance.
        Creates the default configuration file if it doesn't exist.

        Args:
            file_path (str, optional): Path to the JSON configuration file.
                If None, defaults to ~/.config/ai_model_manager/models_api.json.
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
        """
        Internal method to read JSON configuration data from file.

        Returns:
            dict: Parsed JSON data or an empty dict if file not found.
        """
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _write_json(self, data):
        """
        Internal method to write JSON data to file.

        Args:
            data (dict): Data to write into the JSON file.
        """
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def create_default_file(self):
        """
        Creates a configuration file with default model entries.
        Includes a pre-set API key for `gemini-1.5-flash`.
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
        """
        Loads the current configuration from the JSON file.

        Returns:
            dict: Configuration data including selected model and keys.
        """
        return self._read_json()

    def configure_model(self, model_name, api_key):
        """
        Adds or updates a model entry with a given API key.

        Args:
            model_name (str): The name of the model to configure.
            api_key (str): The API key associated with the model.
        """
        data = self._read_json()
        data[model_name] = api_key
        self._write_json(data)
        print("Model added successfully.")

    def remove_model(self, model_name):
        """
        Removes a model from the configuration.

        Args:
            model_name (str): The name of the model to remove.

        Raises:
            ValueError: If the model is not found in the configuration.
        """
        data = self._read_json()
        if model_name in data:
            del data[model_name]
            self._write_json(data)
            print(f"Model '{model_name}' removed successfully.")
        else:
            raise ValueError(f"Model '{model_name}' not found.")

    def get_api_key(self, model_name):
        """
        Retrieves the API key for a given model.

        Args:
            model_name (str): The name of the model.

        Returns:
            str: The API key associated with the model.

        Raises:
            ValueError: If the model is not available or lacks an API key.
        """
        data = self._read_json()
        if model_name in data and data[model_name]:
            return data[model_name]
        raise ValueError(f"Model '{model_name}' is not available or has no API key.")

    def list_models(self):
        """
        Prints the list of models and their corresponding API keys (if available).
        """
        data = self._read_json()
        if data:
            for model, key in data.items():
                print(f"{model}: {key}")
        else:
            print("No models found.")

    def select_model(self, model_name):
        """
        Sets the specified model as the default selected model.

        Args:
            model_name (str): The name of the model to select.

        Prints a message based on whether the selection was successful.
        """
        data = self._read_json()
        if model_name in data and data[model_name]:
            data["selected_model"] = model_name
            self._write_json(data)
            print(f"Selected model: {model_name}")
        else:
            print("No models found or no API key for that model.")

    def generate_output(self, model_name, prompt_by_user):
        """
        Generates LLM output using the specified model and user prompt.

        This method displays a spinner while waiting for a response from the model.

        Args:
            model_name (str): The name of the model to use.
            prompt_by_user (str): The prompt to send to the model.

        Returns:
            str: The model's output.
        """
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(target=spin_loader, args=(stop_spinner,))
        spinner_thread.start()

        output = gemini_api_output(model_name, prompt_by_user)

        stop_spinner.set()
        spinner_thread.join()

        return output
