import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("API key could not be loaded please check .env ")

client = genai.Client(api_key=api_key)

prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

meta_response = response.usage_metadata
if meta_response is None:
    raise RuntimeError("No response metadata... did we lose the connection?")

text_response = response.text


def pretty_output(text, meta):
    return (
        f"User promt: {prompt} \n"
        + f"Prompt tokens: {meta.prompt_token_count} \n"
        + f"Response tokens: {meta.candidates_token_count}\n"
        + f"Response:\n{text}"
    )


def main():
    print("Hello from stuffbot!")
    print(pretty_output(text_response, meta_response))


if __name__ == "__main__":
    main()
