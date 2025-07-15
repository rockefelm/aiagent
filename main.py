import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types



def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt_string>")
        sys.exit(1)
    prompt_string = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt_string)]),
    ]
    print(f"Prompt string: {prompt_string}")
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )
    print(response.text)
    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt_string}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
