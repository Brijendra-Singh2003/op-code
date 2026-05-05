import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions import create_file, list_files, read_file, write_file

load_dotenv()

cwd = os.getcwd()
gemini_api_key = os.getenv("GEMINI_API_KEY")


# Configure the client and tools
client = genai.Client(api_key=gemini_api_key)
tools = types.Tool(
    function_declarations=[
        list_files.list_files_and_directories,
        create_file.create_n_write_file,
        read_file.read_file,
        write_file.apply_patch,
    ]
)
config = types.GenerateContentConfig(tools=[tools])


def chat(s: str, history: list[types.Content]):
    content = types.Content(role="user", parts=[types.Part(text=s)])
    history.append(content)

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=history, config=config
    )

    while response.function_calls:
        history.append(response.candidates[0].content)

        for function_call in response.function_calls:
            print(f"Function to call: {function_call.name}")
            print(f"ID: {function_call.id}")
            print(f"Arguments: {function_call.args}")

            args = function_call.args or {}
            result = None
            match function_call.name:
                case list_files.list_files_and_directories.name:
                    result = list_files.list_files_and_directories_impl(**args)
                case read_file.read_file.name:
                    result = read_file.read_file_impl(**args)
                case write_file.apply_patch.name:
                    result = write_file.apply_patch_impl(**args)
                case create_file.create_n_write_file.name:
                    result = create_file.create_n_write_file_impl(**args)
                case _:
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
