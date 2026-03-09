import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Environment vars and check
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("API key could not be loaded please check .env ")

# Args parse
parser = argparse.ArgumentParser(description="Stuffbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Client and prompt generation
client = genai.Client(api_key=api_key)
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)

meta_response = response.usage_metadata
if meta_response is None:
    raise RuntimeError("No response metadata... did we lose the connection?")

text_response = response.text


# Just an output formatter
def verbose_output(text, meta):
    return (
        f"User prompt: {args.user_prompt} \n"
        + f"Prompt tokens: {meta.prompt_token_count} \n"
        + f"Response tokens: {meta.candidates_token_count}\n"
        + f"Response:\n{text}"
    )


def output(text):
    return f"Response:\n{text}"


# Main
def main():
    print("Hello from stuffbot!")
    if args.verbose:
        print(verbose_output(text_response, meta_response))
    else:
        print(output(text_response))


if __name__ == "__main__":
    main()
