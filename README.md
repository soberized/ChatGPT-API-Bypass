ChatGPT Api Bypass
A Python package designed to automate interactions with ChatGPT without using an API key. This tool allows you to programmatically send prompts to ChatGPT and retrieve responses, including an option to enable web search capabilities if available on the ChatGPT interface.

Features
Undetected Browsing: Uses undetected methods to minimize detection by anti-bot measures.

Prompt Submission: Easily send text prompts to ChatGPT.

Response Retrieval: Extract the full assistant response after generation.

Optional Web Search: Toggle web search functionality for prompts (if supported by ChatGPT's UI at the time of execution).

Installation
You can install chatgpt-automator directly from your local project or via a Git repository link for global access.

Prerequisites
Python 3.8+

Chrome Browser: Ensure you have Google Chrome installed on your system, as this relies on it.

Local Installation (for Development)
If you have cloned the chatgpt-automator repository and want to develop locally, navigate to the root directory of the project (where setup.py is located) and run:

cd chatgpt-automator # Navigate to your project directory
pip install -e .

The -e flag (editable mode) means that any changes you make to the source code will be immediately reflected without needing to reinstall the package.

Standard Installation
To install the package from your local project in a standard way:

cd chatgpt-automator # Navigate to your project directory
pip install .

Global Installation via Git Link
You can install the package directly from a Git repository (e.g., GitHub) using its URL. This allows you to install it globally without cloning the repository first.


pip install git+https://github.com/reproachuwu/chatgpt-api-bypass.git

This command will fetch the package directly from the specified Git repository and install it into your Python environment, making it available system-wide (or within your active virtual environment).

Usage
After installation, you can import and use the launch_chatgpt function in your Python scripts.

from chatgpt_automator import launch_chatgpt

# --- Example 1: Basic Prompt ---
print("--- Running Basic Prompt Example ---")
prompt_basic = "Tell me a short, inspiring quote."
response_basic = launch_chatgpt(prompt_basic)

if response_basic:
    print("\nChatGPT's Response (Basic):")
    print(response_basic)
else:
    print("\nFailed to get a response for the basic prompt.")

# --- Example 2: Prompt with Web Search (if available) ---
# Note: The 'search' parameter attempts to click a web search button on ChatGPT's UI.
# Its effectiveness depends on the current ChatGPT interface and your account's features.
print("\n--- Running Web Search Prompt Example ---")
prompt_search = "What is the capital of Australia and when was it founded? Please search the web for this."
response_search = launch_chatgpt(prompt_search, search=True)

if response_search:
    print("\nChatGPT's Response (with Search):")
    print(response_search)
else:
    print("\nFailed to get a response for the web search prompt.")

print("\nScript finished.")

Function Signature
launch_chatgpt(prompt: str, search: bool = False) -> str | None

prompt (str): The text query you want to send to ChatGPT.

search (bool, optional): If True, the script will attempt to locate and click a "web search" or "browse" button on the ChatGPT interface before sending the prompt. Defaults to False. This functionality is dependent on the ever-changing ChatGPT UI.

Returns: A string containing ChatGPT's response, or None if an error occurred or no response could be retrieved.

Troubleshooting
Browser Not Opening/Connecting: Ensure Chrome is installed and updated.

"Stop streaming" button not disappearing: This might indicate that ChatGPT is taking a very long time to respond, or the response is stuck. The script has a long timeout (180 seconds), but complex queries can exceed this.

Detection Issues: While this is not 100% robust, advanced anti-bot measures can still detect automation in the future.

Contributing
Feel free to open issues or submit pull requests on the GitHub repository if you find bugs, have suggestions, or want to contribute improvements.

License
This project is licensed under the MIT License 