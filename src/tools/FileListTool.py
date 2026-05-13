import os

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
            "required": ["directory_path"],
        },
    },
}


def file_list_impl(directory_path: str = ".") -> dict:
    try:
        return {"success": True, "data": os.listdir(directory_path)}
    except Exception as e:
        return {"success": False, "error": str(e)}
