import asyncio
import os
from asyncio import sleep

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import FileEditTool, FileListTool, FileReadTool, FileWriteTool

load_dotenv()

cwd = os.getcwd()
gemini_api_key = os.getenv("GEMINI_API_KEY")


# Configure the client and tools
client = genai.Client(api_key=gemini_api_key)
tools = types.Tool(
    function_declarations=[
        FileListTool.list_files_and_directories,
        FileWriteTool.create_n_write_file,
        FileReadTool.read_file,
        FileEditTool.apply_patch,
    ]
)
config = types.GenerateContentConfig(tools=[tools])
history: list[types.Content] = []


async def get_response():
    sleep_duration = 8
    while True:
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview", contents=history, config=config
            )

            return response
        except Exception as e:
            print(f"error: {str(e)}")
            sleep_duration *= 2
            await sleep(sleep_duration)


async def main():
    while True:
        s = input("> ")
        content = types.Content(role="user", parts=[types.Part(text=s)])
        history.append(content)

        response = await get_response()

        while response.function_calls:
            candidate = response.candidates[0] if response.candidates else None
            if candidate and candidate.content:
                history.append(candidate.content)

            for function_call in response.function_calls:
                print(f"Function to call: {function_call.name}")
                print(f"ID: {function_call.id}")
                print(f"Arguments: {function_call.args}")

                args = function_call.args or {}
                result = None
                match function_call.name:
                    case FileListTool.list_files_and_directories.name:
                        result = FileListTool.list_files_and_directories_impl(**args)
                    case FileReadTool.read_file.name:
                        result = FileReadTool.read_file_impl(**args)
                    case FileEditTool.apply_patch.name:
                        result = FileEditTool.apply_patch_impl(**args)
                    case FileWriteTool.create_n_write_file.name:
                        result = FileWriteTool.create_n_write_file_impl(**args)
                    case _:
                        result = None

                print(f"Result: {result}")

                function_response_part = types.Part.from_function_response(
                    name=function_call.name or "",
                    response={"result": result},
                )

                history.append(
                    types.Content(role="user", parts=[function_response_part])
                )

            response = await get_response()

        history.append(
            types.Content(role="model", parts=[types.Part(text=response.text)])
        )
        print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
