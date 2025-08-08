import os
import sys
import argparse
from cli.ai_model_manager import AIModelManager
from cli.chat_history import ChatHistory, get_bash_history
from cli.llm import generate_response

HISTORY_FILE = os.path.expanduser("~/.cache/cli_chat_history.json")
DEFAULT_BASH_HISTORY_COUNT = 3


def handle_command(args, manager, history):
    """Handle different CLI commands."""
    if args.command == "chat":
        prompt_text = " ".join(args.text)
        generate_response(prompt_text, manager, history)
        
    elif args.command == "debug":
        bash = get_bash_history(args.number)
        dprompt = f"{bash}{args.prompt or ''} output what is wrong with the commands used and suggest correct ones"
        generate_response(dprompt, manager, history)
        
    elif args.command == "config":
        if not manager.validate_model(args.model):
            print(f"❌ '{args.model}' is not supported. Use 'tex models' to see all models.")
            return
        manager.configure_model(args.model, args.key)
        
    elif args.command == "list":
        manager.list_models()
        
    elif args.command == "models":
        print("🚀 All supported models:")
        manager.print_supported_models()
        
    elif args.command == "remove":
        manager.remove_model(args.model)
        
    elif args.command == "select":
        if not manager.validate_model(args.model):
            print(f"❌ '{args.model}' is not supported. Use 'tex models' to see all models.")
            return
        manager.select_model(args.model)
        
    elif args.command == "validate":
        manager.validate_all_models()
        
    else:
        print("❌ Unknown command. Use 'tex --help' for available commands.")


def main():
    raw = sys.argv[1:]
    known_cmds = ["chat", "debug", "config", "list", "remove", "select", "models", "validate"]

    manager = AIModelManager()
    history = ChatHistory(HISTORY_FILE)

    # Handle setup shortcut
    if raw and raw[0] == "--setup":
        manager.create_default_file()
        return

    # Handle direct chat (no subcommand)
    if raw and raw[0] not in known_cmds and not raw[0].startswith("-"):
        prompt_text = " ".join(raw)
        generate_response(prompt_text, manager, history)
        return

    # Parse commands
    parser = argparse.ArgumentParser(prog="tex", description="🤖 Multi-model CLI for AI chat")
    parser.add_argument("--setup", action="store_true", help="Create default config")
    subparsers = parser.add_subparsers(dest="command")

    # Define subcommands
    chat_parser = subparsers.add_parser("chat", help="Chat with AI")
    chat_parser.add_argument("text", nargs="+", help="Your message")

    debug_parser = subparsers.add_parser("debug", help="Debug bash commands") 
    debug_parser.add_argument("-n", "--number", type=int, default=DEFAULT_BASH_HISTORY_COUNT, help="Number of commands")
    debug_parser.add_argument("-p", "--prompt", type=str, help="Additional context")

    config_parser = subparsers.add_parser("config", help="Configure model API key")
    config_parser.add_argument("model", help="Model name")
    config_parser.add_argument("key", help="API key")

    subparsers.add_parser("list", help="List configured models")
    subparsers.add_parser("models", help="Show all supported models")

    remove_parser = subparsers.add_parser("remove", help="Remove model")
    remove_parser.add_argument("model", help="Model name")

    select_parser = subparsers.add_parser("select", help="Select active model")
    select_parser.add_argument("model", help="Model name")

    subparsers.add_parser("validate", help="Test all configured models")

    args = parser.parse_args(raw)

    if args.setup:
        manager.create_default_file()
    elif args.command:
        handle_command(args, manager, history)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
