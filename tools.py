from google.genai import types

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


tools = types.Tool(
    function_declarations=[list_files_and_directories, read_file, write_file]
)
