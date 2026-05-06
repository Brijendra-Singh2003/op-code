import os

from .result import err, ok

file_list_tool = {
    "type": "function",
    "function": {
        "name": "file_list",
        "description": "reads and returns a list of all the folders and files present in a given folder.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory_path": {
                    "type": "string",
                    "description": "path of the directory to list.",
                }
            },
            "required": [],
        },
    },
}


def file_list_impl(directory_path: str = ".") -> dict:
    try:
        return ok(os.listdir(directory_path)).to_dict()
    except Exception as e:
        return err(str(e)).to_dict()
