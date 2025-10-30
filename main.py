import os
from dotenv import load_dotenv
import sys

from google import genai 
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt
from config import MAX_LOOPS


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

    loop_count = 0

    if verbose:
        print(f'User prompt: {user_prompt}\n')

    while loop_count < MAX_LOOPS:
        loop_count += 1
        if verbose:
            print(f"\n--- Loop {loop_count}/{MAX_LOOPS} ---\n")
            
        response: genai.models.GenerateContentResponse = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt),
        )

        if verbose:
            for candidate in response.candidates:
                print(f"Candidate: {candidate.content}")
        
        # Add the model's response to messages
        messages.append(response.candidates[0].content)

        # Check if there are function calls to execute
        function_called = False
        function_responses = []
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.function_call is not None:
                    function_called = True
                    args_str = ", ".join(f"'{k}': '{v}'" for k, v in part.function_call.args.items())
                    print(f"Calling function: {part.function_call.name}({args_str})")
                    try:
                        function_call_result = call_function(part.function_call, verbose=verbose)
                        function_responses.append(function_call_result.parts[0])
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    except Exception as e:
                        if verbose:
                            print(f"Error executing function: {e}")
        
        # If functions were called, add all responses in a single message
        if function_called:
            messages.append(types.Content(
                role="tool",
                parts=function_responses
            ))
        
        # If no function was called, the model has given its final response
        if not function_called:
            if response.text:
                if verbose:
                    print(f"\nAI Response: {response.text}\n")
                else:
                    print(f"\n{response.text}")
            break
    
    if loop_count >= MAX_LOOPS:
        print(f"\nReached maximum loop count ({MAX_LOOPS})")
    
    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')



if __name__ == "__main__":
    main()
