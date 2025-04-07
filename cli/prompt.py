import os
import sys
from cli.ai_model_manager import AIModelManager
from cli.prettify_llm_output import prettify_llm_output

manager = AIModelManager()


def user_command_line_prompt():
    """
    Parses command-line arguments to separate the user's prompt and any additional flags.

    Returns:
        tuple: A tuple containing the user's prompt (str or None) and a list of input flags.
    """
    args = [x for x in sys.argv]

    if len(args) > 1 and not args[1].startswith("--"):
        prompt_by_user = args[1]
        entire_cmd_command = " ".join(args[2:])
    else:
        prompt_by_user = None
        entire_cmd_command = " ".join(args[1:])

    all_input_flags = entire_cmd_command.split("--")
    all_input_flags = [x.strip() for x in all_input_flags]

    return prompt_by_user, all_input_flags


def last_command_line_prompt(last_number_of_commands):
    """
    Retrieves the last N commands from the user's bash history.

    Args:
        last_number_of_commands (int): Number of recent commands to retrieve.

    Returns:
        str: The last N commands as a single string.
    """
    history_file = os.path.expanduser("~/.bash_history")
    with open(history_file, "r") as file:
        history_lines = file.readlines()
    last_commands = history_lines[-last_number_of_commands:]
    return "".join(last_commands)


def prompt_for_llm(prompt_for_llm):
    """
    Sends a prompt to the selected LLM model and prints the response.

    Args:
        prompt_for_llm (str): The prompt to send to the model.
    """
    prompt_for_llm += " give response in short form, if asked for commands then give commands and dont explain too much"
    models_api_dict = manager.load()
    model_name = models_api_dict["selected_model"] or "gemini-1.5-flash"
    response = manager.generate_output(model_name, prompt_for_llm)
    prettify_llm_output(response)


def debug_last_command_line_prompt(prompt_by_user, all_input_flags):
    """
    Analyzes and debugs the last few command-line commands using the LLM.

    Args:
        prompt_by_user (str or None): Optional user prompt to append.
        all_input_flags (list): List of input flags provided in the CLI.
    """
    last_number_of_commands = (
        int(all_input_flags[2]) if len(all_input_flags) == 3 else 3
    )
    if prompt_by_user:
        prompt_by_vertex = (
            last_command_line_prompt(last_number_of_commands)
            + prompt_by_user
            + " basically output what is wrong with the commands used and suggest right ones"
        )
    else:
        prompt_by_vertex = (
            last_command_line_prompt(last_number_of_commands)
            + " output what is wrong with the commands used and suggest right ones, don’t explain about tex command"
        )
    print("Prompt by vertex:", prompt_by_vertex)
    print()
    prompt_for_llm(prompt_by_vertex)


def handle_input_flags(all_input_flags):
    """
    Handles input flags such as configuring, removing, selecting, or listing models.

    Args:
        all_input_flags (list): List of input flags from the CLI.
    """
    if all_input_flags:
        if not all_input_flags[0] == "":
            print(
                "Prompt should be quoted in double quotes, and the flags must be spaced out"
            )

        for flag in all_input_flags:
            flags_list = flag.split(" ")
            if flag.startswith("config"):
                manager.configure_model(flags_list[1], flags_list[2])
                print(
                    f"Configured model: {flags_list[1]} with API key: {flags_list[2]}"
                )
            elif flag == "list":
                print("Listing all models:")
                manager.list_models()
            elif flag.startswith("remove"):
                print("Removing model:", flags_list[1])
                manager.remove_model(flags_list[1])
            elif flag.startswith("select"):
                manager.select_model(flags_list[1])
            elif flag == "help":
                print("Usage: python3 main.py <prompt>")
                print("Example: python3 main.py 'How are you?'")
                print("Flags are: --config <model_name> <api_key>, remove <model_name>")
                print()


def handle_all_quries():
    """
    Main logic to handle prompt input, debugging, or flag-based commands from the CLI.
    """
    prompt_by_user, all_input_flags = user_command_line_prompt()
    if prompt_by_user:
        prompt_for_llm(prompt_by_user)
    elif len(all_input_flags) > 1 and all_input_flags[1] == "debug":
        debug_last_command_line_prompt(prompt_by_user, all_input_flags)
    handle_input_flags(all_input_flags)


def main():
    """
    Entry point for the CLI tool. Initializes config file or processes CLI inputs.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        manager.create_default_file()
    else:
        handle_all_quries()


if __name__ == "__main__":
    main()
