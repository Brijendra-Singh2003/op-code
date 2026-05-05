import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

cwd = os.getcwd()
gemini_api_key = os.getenv("GEMINI_API_KEY")


# Configure the client and tools
client = genai.Client(api_key=gemini_api_key)
tools = types.Tool(function_declarations=[])
config = types.GenerateContentConfig(tools=[tools])


def chat(s: str, history: list[types.Content]):
    content = types.Content(role="user", parts=[types.Part(text=s)])
    history.append(content)

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=history, config=config
    )

    while response.function_calls:
        candidate = response.candidates[0] if response.candidates else None
        if candidate and candidate.content:
            history.append(candidate.content)

        for function_call in response.function_calls:
            print(f"Function to call: {function_call.name}")
            print(f"ID: {function_call.id}")
            print(f"Arguments: {function_call.args}")

            result = None
            print(f"Result: {result}")

            function_response_part = types.Part.from_function_response(
                name=function_call.name or "",
                response={"result": result},
            )

            history.append(types.Content(role="user", parts=[function_response_part]))

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config=config,
            contents=history,
        )

    history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
    return response.text
