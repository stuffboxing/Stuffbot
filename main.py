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

client = genai.Client(api_key=api_key)


def output(text):
    return f"Response:\n{text}\n"


def verbose_output(text, meta, tool_results):
    rvalue = (
        f"User prompt: {args.user_prompt} \n"
        f"Prompt tokens: {meta.prompt_token_count} \n"
        f"Response tokens: {meta.candidates_token_count}\n"
        f"Response:\n{text}"
    )
    for tool_result in tool_results:
        rvalue += (
            f"\nCalling function: {tool_result['name']}({tool_result['args']})\n"
            f"-> {tool_result['response']}"
        )
    return rvalue


def extract_function_response(func_result, call):
    if not func_result.parts:
        raise Exception(f"Error: No parts in function result for call {call}")
    if not func_result.parts[0].function_response:
        raise Exception(f"Error: function response of call {call} was none")
    if not func_result.parts[0].function_response.response:
        raise Exception(f"Error: response of function response of call {call} was none")
    return func_result.parts[0].function_response.response


def run_agent_loop():
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    tool_results = []
    response = None

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
            ),
        )

        candidate_content = None
        if response.candidates:
            candidate_content = response.candidates[0].content
        if candidate_content is not None:
            messages.append(candidate_content)

        function_calls = response.function_calls or []
        if not function_calls:
            return response, tool_results

        for call in function_calls:
            func_result = call_function(call, verbose=args.verbose)
            function_response = extract_function_response(func_result, call)
            tool_results.append(
                {
                    "name": call.name,
                    "args": dict(call.args) if call.args else {},
                    "response": function_response,
                }
            )
            messages.append(func_result)

    raise SystemExit(1)


# Main
def main():
    print("Hello from stuffbot!")
    response, tool_results = run_agent_loop()
    meta_response = response.usage_metadata
    if meta_response is None:
        raise Exception("No response metadata... did we lose the connection?")
    text_response = response.text or ""

    if args.verbose:
        print(verbose_output(text_response, meta_response, tool_results))
    else:
        print(output(text_response))


if __name__ == "__main__":
    main()
