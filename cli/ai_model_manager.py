import json
import os
import threading
from cli.utils import spin_loader
from cli.llm_providers import LLMProviderFactory


class AIModelManager:
    """Simplified AI model manager with multi-provider support."""

    def __init__(self, file_path=None):
        if file_path is None:
            config_dir = os.path.join(os.path.expanduser("~"), ".config", "ai_model_manager")
            os.makedirs(config_dir, exist_ok=True)
            file_path = os.path.join(config_dir, "models_api.json")

        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self.create_default_file()

    def _read_json(self):
        try:
            with open(self.file_path, "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _write_json(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def create_default_file(self):
        """Create default configuration with popular models."""
        default_config = {
            "selected_model": None,
            # Popular models with None API keys (to be configured by user)
            "gpt-4o": None,
            "gpt-3.5-turbo": None,
            "claude-3-5-sonnet": None,
            "gemini-1.5-flash": "AIzaSyCSXtRAITXfGuarMHI1j-0QyKkoT9mUfz8",  # Keep existing key
        }
        self._write_json(default_config)
        print(f"Config file created at: {self.file_path}")

    def load(self):
        return self._read_json()

    def configure_model(self, model_name, api_key):
        if not self.validate_model(model_name):
            raise ValueError(f"Unsupported model: {model_name}")
        
        # Warn about test keys
        if self._is_test_key(api_key):
            print(f"⚠️  Warning: '{api_key}' looks like a test key. Please use your actual API key.")
            print(f"   Get your real API key from the provider's website.")
        
        data = self._read_json()
        data[model_name] = api_key
        self._write_json(data)
        print(f"✅ {model_name} configured successfully.")

    def _is_test_key(self, api_key):
        """Check if the API key looks like a test key."""
        test_patterns = ["test", "fake", "dummy", "example", "demo", "placeholder", "your_api_key"]
        return any(pattern in api_key.lower() for pattern in test_patterns)

    def remove_model(self, model_name):
        data = self._read_json()
        if model_name in data and model_name != "selected_model":
            del data[model_name]
            # Reset selection if this was the selected model
            if data.get("selected_model") == model_name:
                data["selected_model"] = None
            self._write_json(data)
            print(f"✅ {model_name} removed successfully.")
        else:
            print(f"❌ Model '{model_name}' not found.")

    def get_api_key(self, model_name):
        data = self._read_json()
        if model_name in data and data[model_name]:
            return data[model_name]
        raise ValueError(f"Model '{model_name}' is not configured or has no API key.")

    def list_models(self):
        data = self._read_json()
        print("📋 Configured models:")
        for model, key in data.items():
            if model == "selected_model":
                continue
            provider = LLMProviderFactory.get_provider_for_model(model)
            status = "✅" if key else "❌"
            selected = "👈 SELECTED" if data.get("selected_model") == model else ""
            print(f"  {status} {model} ({provider}) {selected}")

    def select_model(self, model_name):
        if not self.validate_model(model_name):
            print(f"❌ '{model_name}' is not a supported model.")
            return False
            
        data = self._read_json()
        if model_name not in data or not data[model_name]:
            print(f"❌ '{model_name}' is not configured. Configure it first with:")
            print(f"    tex config {model_name} YOUR_API_KEY")
            return False
            
        data["selected_model"] = model_name
        self._write_json(data)
        print(f"✅ Selected model: {model_name}")
        return True

    def generate_output(self, model_name, prompt_by_user, system_instruction=None):
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(target=spin_loader, args=(stop_spinner,))
        spinner_thread.start()

        try:
            api_key = self.get_api_key(model_name)
            provider = LLMProviderFactory.create_provider(model_name, api_key)
            output = provider.generate_response(prompt_by_user, system_instruction)
        except Exception as e:
            output = f"❌ Error: {str(e)}"
        finally:
            stop_spinner.set()
            spinner_thread.join()

        return output

    def validate_model(self, model_name):
        return LLMProviderFactory.is_model_supported(model_name)

    def get_available_models(self):
        data = self._read_json()
        return [model for model, key in data.items() 
                if model != "selected_model" and key]

    def get_supported_models(self):
        return LLMProviderFactory.get_supported_models()

    def print_supported_models(self):
        supported = self.get_supported_models()
        for provider, models in supported.items():
            print(f"\n🔹 {provider.upper()}:")
            for model in models:
                print(f"  • {model}")

    def validate_all_models(self):
        """Test all configured models with a simple prompt."""
        print("🧪 Testing all configured models...")
        data = self._read_json()
        configured_models = [(model, key) for model, key in data.items() 
                           if model != "selected_model" and key]
        
        if not configured_models:
            print("❌ No models configured. Use 'tex config MODEL_NAME API_KEY' to add models.")
            return
        
        test_prompt = "Hello! Please respond with 'OK' to confirm you're working."
        
        for model_name, api_key in configured_models:
            print(f"\n🔍 Testing {model_name}...")
            
            if self._is_test_key(api_key):
                print(f"  ⚠️  Skipped - test key detected: {api_key[:10]}...")
                continue
                
            try:
                response = self.generate_output(model_name, test_prompt)
                if response.startswith("❌"):
                    print(f"  ❌ Failed: {response}")
                else:
                    print(f"  ✅ Working: {response.strip()[:50]}...")
            except Exception as e:
                print(f"  ❌ Error: {str(e)[:100]}...")
        
        print("\n💡 To fix issues:")
        print("   • Get real API keys from provider websites")
        print("   • Run: tex config MODEL_NAME YOUR_REAL_API_KEY")
        print("   • Check quota/billing on provider dashboards")
