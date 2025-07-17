import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
from functions.write_file import *
from functions.get_file_content import *
from functions.run_python import *
from functions.call_function import call_function


def main():
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    You should check through your tools first if your short on information.
    If you identify the next step to take, you should do that.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt_string>")
        sys.exit(1)
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_get_file_content,
            schema_run_python_file,
        ]
    )
    prompt_string = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt_string)]),
    ]
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)



    iterations = 0
    while True:
        iterations += 1
        if iterations > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
        
        try:

            response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
                ),
            )
            for candidate in response.candidates:
                function_call_content = candidate.content
                messages.append(function_call_content)

            if response.text and not response.function_calls:
                print(f"Response: {response.text}")
                break

            function_responses = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, "--verbose" in sys.argv)
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("empty function call result")
            if "--verbose" in sys.argv:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(types.Content(role="tool", parts=[function_call_result.parts[0]]))

            if not function_responses:
                raise Exception("no function responses generated, exiting.")
            messages.extend(function_responses)
        except Exception as e:
            print(f"Error in generate_content: {e}")

    if "--verbose" in sys.argv:
        print(f"Prompt string: {prompt_string}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    



if __name__ == "__main__":
    main()
