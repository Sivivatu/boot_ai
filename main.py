import os
from dotenv import load_dotenv
import sys

from google import genai
from google.genai import types



# prompt: str = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

def main() -> None:
    load_dotenv()

    verbose: bool = "--verbose" in sys.argv
    args: list[str] = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    user_prompt: str = sys.argv[1] if len(sys.argv) > 1 else None
    if not args:
        # exit if no prompt is provided
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print("Please provide a prompt as a command line argument.")
        sys.exit(1)
    
    api_key: str | None = os.getenv("GEMINI_API_KEY")

    messages: list[types.Content] = [
        types.Content(role="user",
        parts=[types.Part(text=user_prompt)]
        )
    ]
    client = genai.Client(
        api_key=api_key,
    )

    response: genai.models.GenerateContentResponse = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
    )


    if verbose:
        print(f'User prompt: {user_prompt}\n')
    print(response.text)    
    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count }')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count }')



if __name__ == "__main__":
    main()
