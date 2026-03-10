import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function
from prompts import system_prompt

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
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions],
    ),
)

meta_response = response.usage_metadata
if meta_response is None:
    raise RuntimeError("No response metadata... did we lose the connection?")

text_response = response.text
fn_call = response.function_calls


# Just an output formatter
def verbose_output(text, meta, calls=None):
    f_result_list = []
    rvalue = (
        f"User prompt: {args.user_prompt} \n"
        f"Prompt tokens: {meta.prompt_token_count} \n"
        f"Response tokens: {meta.candidates_token_count}\n"
        f"Response:\n{text}"
    )
    if calls:
        for call in calls:
            func_result = call_function(call, verbose=True)
            if not func_result.parts:
                raise Exception(f"Error: No parts in function result for call {call}")
            if not func_result.parts[0].function_response:
                raise Exception(f"Error: functions response of call {call} was none")
            if not func_result.parts[0].function_response.response:
                raise Exception(
                    f"Error: Response of function_repsonse of call {call} was none"
                )
            f_result_list.append(func_result.parts[0])
            rvalue += f"-> {func_result.parts[0].function_response.response}\n"
    return rvalue


def output(text, calls=None):
    rvalue = f"Response:\n{text}\n"
    f_result_list = []
    if calls:
        for call in calls:
            func_result = call_function(call, verbose=False)
            if not func_result.parts:
                raise Exception(f"Error: No parts in function result for call {call}")
            if not func_result.parts[0].function_response:
                raise Exception(f"Error: functions response of call {call} was none")
            if not func_result.parts[0].function_response.response:
                raise Exception(
                    f"Error: Response of function_repsonse of call {call} was none"
                )
            f_result_list.append(func_result.parts[0])
    return rvalue


# Main
def main():
    print("Hello from stuffbot!")
    if args.verbose:
        print(verbose_output(text_response, meta_response, fn_call))
    else:
        print(output(text_response, fn_call))


if __name__ == "__main__":
    main()
