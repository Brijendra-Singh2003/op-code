import os

from google.genai import types

list_files_and_directories = types.FunctionDeclaration(
    name="list_files_and_directories",
    description="reads and returns a list of all the folders and files present in a given folder.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory_path": types.Schema(
                type=types.Type.STRING,
                description="optional parameter to specify path of the directory you want to get the files & nested directories of.",
                example="src/common",
                default=".",
            )
        },
        required=[],
    ),
    response=types.Schema(
        type=types.Type.ARRAY, description="list of files and directories."
    ),
)


def list_files_and_directories_impl(directory_path: str = ".") -> list | dict:
    try:
        return os.listdir(directory_path)
    except Exception as e:
        return {"error": str(e)}
