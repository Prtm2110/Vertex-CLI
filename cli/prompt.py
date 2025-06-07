import os
import json
import sys
import argparse
from cli.ai_model_manager import AIModelManager
from cli.prettify_llm_output import prettify_llm_output

HISTORY_FILE = os.path.expanduser("~/.cache/cli_chat_history.json")
DEFAULT_HISTORY_SIZE = 10
DEFAULT_BASH_HISTORY_COUNT = 3


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
        return "".join(
            f"{item['role'].capitalize()}: {item['content']}\n" for item in self.history
        )

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


def main():
    raw = sys.argv[1:]
    known_cmds = ["chat", "debug", "config", "list", "remove", "select"]

    manager = AIModelManager()
    history = ChatHistory(HISTORY_FILE)

    # Setup shortcut
    if raw and raw[0] == "--setup":
        manager.create_default_file()
        print("Default configuration created.")
        return

    # Default chat if no subcommand
    if raw and raw[0] not in known_cmds:
        prompt_text = " ".join(raw)
        generate_response(prompt_text, manager, history)
        return

    # Subcommand parsing
    parser = argparse.ArgumentParser(
        prog="tex", description="CLI for interacting with LLMs"
    )
    parser.add_argument("--setup", action="store_true", help="Create default config")
    subparsers = parser.add_subparsers(dest="command")

    # chat
    chat_parser = subparsers.add_parser("chat", help="Send a prompt to the LLM")
    chat_parser.add_argument("text", nargs="+", help="Prompt text")

    # debug
    debug_parser = subparsers.add_parser("debug", help="Debug recent bash commands")
    debug_parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=DEFAULT_BASH_HISTORY_COUNT,
        help="Number of recent commands",
    )
    debug_parser.add_argument(
        "-p", "--prompt", type=str, help="Additional explanation prompt"
    )

    # config
    config_parser = subparsers.add_parser("config", help="Configure a model API key")
    config_parser.add_argument("model", help="Model name")
    config_parser.add_argument("key", help="API key")

    # list
    subparsers.add_parser("list", help="List configured models")

    # remove
    remove_parser = subparsers.add_parser("remove", help="Remove a configured model")
    remove_parser.add_argument("model", help="Model name")

    # select
    select_parser = subparsers.add_parser("select", help="Select active model")
    select_parser.add_argument("model", help="Model name")

    args = parser.parse_args(raw)

    if args.setup:
        manager.create_default_file()
        print("Default configuration created.")

    elif args.command == "chat":
        prompt_text = " ".join(args.text)
        generate_response(prompt_text, manager, history)

    elif args.command == "debug":
        bash = get_bash_history(args.number)
        dprompt = f"{bash}{args.prompt or ''} "
        dprompt += (
            "output what is wrong with the commands used and suggest correct ones"
        )
        generate_response(dprompt, manager, history)

    elif args.command == "config":
        manager.configure_model(args.model, args.key)

    elif args.command == "list":
        print("Configured models:")
        manager.list_models()

    elif args.command == "remove":
        manager.remove_model(args.model)

    elif args.command == "help":
        parser.print_help()

    elif args.command == "select":
        manager.select_model(args.model)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
