import os
from dotenv import load_dotenv
import sys

from google import genai 
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main() -> None:
    load_dotenv()

    verbose: bool = "--verbose" in sys.argv
    args: list[str] = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        # exit if no prompt is provided
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print("Please provide a prompt as a command line argument.")
        sys.exit(1)
    
    api_key: str | None = os.getenv("GEMINI_API_KEY")

    model_name = 'gemini-2.0-flash-001'



    user_prompt: str = " ".join(args)

    messages: list[types.Content] = [
        types.Content(role="user",
        parts=[types.Part(text=user_prompt)]
        )
    ]
    client = genai.Client(
        api_key=api_key,
    )

    response: genai.models.GenerateContentResponse = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools= [available_functions],
            system_instruction=system_prompt),
    )


    if verbose:
        print(f'User prompt: {user_prompt}\n')
    function_called: bool= False

    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if function_called := part.function_call is not None:
                args_str = ", ".join(f"'{k}': '{v}'" for k, v in part.function_call.args.items())
                print(f"Calling function: {part.function_call.name}({args_str})")
                try:
                    function_call_result = call_function(part.function_call, verbose=verbose)
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                except Exception:
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                function_called = True
                break
    
    if not function_called:
        print(response.text)    
    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count }')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count }')



if __name__ == "__main__":
    main()
