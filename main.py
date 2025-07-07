from http import client
import os
from dotenv import load_dotenv

from google import genai

# Load environment variables from a .env file

load_dotenv()

api_key: str | None = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key,
)


prompt: str = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

def main() -> None:
    response: genai.models.GenerateContentResponse = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=prompt
    )
    print(response.text)    
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count }')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count }')


if __name__ == "__main__":
    main()
