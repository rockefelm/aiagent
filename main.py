import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *


def main():
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt_string>")
        sys.exit(1)
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )
    prompt_string = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt_string)]),
    ]
    print(f"Prompt string: {prompt_string}")
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.function_calls:
        for function in response.function_calls:
            if function.name == "get_files_info":
                directory = function.args.get("directory", ".")
                print(f"Calling function: {function.name}({function.args})")
                print(get_files_info(os.getcwd(), directory))         
    else:
        print(response.text)
    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt_string}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
