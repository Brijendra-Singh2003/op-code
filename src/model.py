import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

cwd = os.getcwd()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Define the function declaration for the model
list_files_and_directories = {
    "name": "list_files_and_directories",
    "description": "reads and returns a list of all the folders and files present in a given folder.",
    "parameters": {
        "type": "object",
        "properties": {
            "directory_path": {
                "type": "string",
                "description": "optional parameter to specify path of the directory you want to get the files & nested directories of (e.g. src/main.py). Defaults to current working directory",
            },
        },
        "required": [],
    },
}
read_file = {
    "name": "read_file",
    "description": "reads and returns the content of a file.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "relative or absolute path of the file you want to read (e.g. src/main.py).",
            },
        },
        "required": ["file_path"],
    },
}
write_file = {
    "name": "write_file",
    "description": "writes the content of a file.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "path of the file you want to write to (e.g. src/main).",
            },
            "content": {
                "type": "string",
                "description": "content you want to write into the file (e.g. src/main).",
            },
        },
        "required": ["file_path", "content"],
    },
}


def list_files_and_directories_impl(directory_path: str = ".") -> list | dict:
    """reads and returns all the folders and files present in a given folder."""
    import os

    try:
        return os.listdir(directory_path)
    except Exception as e:
        return {"error": str(e)}


def read_file_impl(file_path: str) -> str | dict:
    """reads and returns the content of a file."""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return {"error": str(e)}


def write_file_impl(file_path: str, content: str) -> dict:
    """writes the content of a file."""
    try:
        with open(file_path, "w") as f:
            f.write(content)
        return {"status": "success", "message": f"File written to {file_path}"}
    except Exception as e:
        return {"error": str(e)}


# Configure the client and tools
client = genai.Client(api_key=gemini_api_key)
# tools = types.Tool(function_declarations=[list_files_and_directories, read_file, write_file])
tools = types.Tool(function_declarations=[])
config = types.GenerateContentConfig(tools=[tools])
histories: dict[int, list[types.Content]] = dict()


def chat(user_id: int, s: str):
    if user_id not in histories:
        histories[user_id] = []

    history = histories[user_id]
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
                case "list_files_and_directories":
                    result = list_files_and_directories_impl(**args)
                case "read_file":
                    result = read_file_impl(**args)
                case "write_file":
                    result = write_file_impl(**args)
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
