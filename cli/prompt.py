"""CLI entry point for Vertex-CLI."""

import os
import sys
import argparse
from cli.config_manager import ConfigurationManager
from cli.llm_service import LLMService
from cli.chat_history import ChatHistory, get_bash_history
from cli.llm import generate_response

HISTORY_FILE = os.path.expanduser("~/.cache/cli_chat_history.json")
DEFAULT_BASH_HISTORY_COUNT = 3


def main():
    """Main CLI entry point."""
    raw = sys.argv[1:]
    known_cmds = ["chat", "debug", "config", "list", "remove", "select"]

    # Initialize services
    config_manager = ConfigurationManager()
    llm_service = LLMService(config_manager)
    history = ChatHistory(HISTORY_FILE)

    # Setup shortcut
    if raw and raw[0] == "--setup":
        config_manager._create_default_config()
        print("Default configuration created.")
        return

    # Default chat if no subcommand
    if raw and raw[0] not in known_cmds:
        prompt_text = " ".join(raw)
        generate_response(prompt_text, llm_service, history)
        return

    # Subcommand parsing
    parser = argparse.ArgumentParser(
        prog="tex", description="CLI for interacting with multiple LLMs via LangChain"
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
    debug_parser.add_argument("-p", "--prompt", type=str, help="Additional explanation prompt")

    # config
    config_parser = subparsers.add_parser(
        "config", help="Configure a model (usage: config <model> <api_key>)"
    )
    config_parser.add_argument("model", help="Model name (e.g., gemini-2.5-flash, gpt-4)")
    config_parser.add_argument("key", help="API key")
    config_parser.add_argument(
        "--provider", type=str, help="Provider name (auto-detected if not specified)"
    )
    config_parser.add_argument(
        "--temperature", type=float, default=0.7, help="Temperature (0.0-1.0)"
    )

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
        config_manager._create_default_config()
        print("Default configuration created.")

    elif args.command == "chat":
        prompt_text = " ".join(args.text)
        generate_response(prompt_text, llm_service, history)

    elif args.command == "debug":
        bash = get_bash_history(args.number)
        dprompt = f"{bash}{args.prompt or ''} "
        dprompt += "output what is wrong with the commands used and suggest correct ones"
        generate_response(dprompt, llm_service, history)

    elif args.command == "config":
        # Auto-detect provider if not specified
        provider = args.provider
        if not provider:
            model_lower = args.model.lower()
            if "gemini" in model_lower:
                provider = "google"
            elif "gpt" in model_lower or "openai" in model_lower:
                provider = "openai"
            elif "claude" in model_lower:
                provider = "anthropic"
            else:
                print(f"Could not auto-detect provider for '{args.model}'")
                print("Please specify provider with --provider")
                print("Available: google, openai, anthropic")
                return

        config_manager.set_model_config(
            model_name=args.model,
            provider=provider,
            api_key=args.key,
            temperature=args.temperature,
        )

    elif args.command == "list":
        print("\nConfigured models:")
        print("-" * 60)
        models = config_manager.list_models()
        selected = config_manager.get_selected_model()

        if not models:
            print("No models configured.")
        else:
            for name, config in models.items():
                selected_marker = " [SELECTED]" if name == selected else ""
                api_key_status = "✓" if config.get("api_key") else "✗"
                print(f"{name}{selected_marker}")
                print(f"  Provider: {config.get('provider', 'N/A')}")
                print(f"  API Key: {api_key_status}")
                print(f"  Temperature: {config.get('temperature', 0.7)}")
                print()

    elif args.command == "remove":
        try:
            config_manager.remove_model(args.model)
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "select":
        try:
            config_manager.set_selected_model(args.model)
        except ValueError as e:
            print(f"Error: {e}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
