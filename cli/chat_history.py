import os
import json

DEFAULT_HISTORY_SIZE = 10


class ChatHistory:
    def __init__(self, path: str, max_length: int = DEFAULT_HISTORY_SIZE):
        self.path = path
        self.max_length = max_length
        self._ensure_file()
        self._load()

    def _ensure_file(self):
        parent = os.path.dirname(self.path)
        os.makedirs(parent, exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def _load(self):
        try:
            with open(self.path, "r") as f:
                self.history = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.history = []

    def append(self, role: str, content: str):
        entry = {"role": role, "content": content}
        self.history.append(entry)
        self.history = self.history[-self.max_length :]
        self._save()

    def get_prompt(self) -> str:
        return "".join(f"{item['role'].capitalize()}: {item['content']}\n" for item in self.history)

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.history, f, indent=2)


def get_bash_history(count: int) -> str:
    history_file = os.path.expanduser("~/.bash_history")
    try:
        with open(history_file, "r") as f:
            lines = f.readlines()
        return "".join(lines[-count:])
    except IOError:
        return ""
