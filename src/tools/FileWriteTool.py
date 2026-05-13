import os

file_write_tool = {
    "type": "function",
    "function": {
        "name": "file_write",
        "description": "creates a file at a given location and returns its path.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {"type": "string", "description": "name of the file."},
                "folder_path": {
                    "type": "string",
                    "description": "path where to create the file",
                },
                "content": {
                    "type": "string",
                    "description": "content to initialize file with",
                },
            },
            "required": ["file_name", "folder_path", "content"],
        },
    },
}


def file_write_impl(file_name: str, folder_path: str = ".", content: str = "") -> dict:
    print(
        f"\n[confirm] create_n_write_file(file_name={file_name!r}, folder_path={folder_path!r})"
    )
    if input("Allow? [y/N] ").strip().lower() != "y":
        return {"success": False, "error": "user denied permission"}
    try:
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            return {"success": False, "error": f"file already exists: {file_path}"}
        with open(file_path, "w") as f:
            f.write(content)
        return {"success": True, "data": file_path}
    except Exception as e:
        return {"success": False, "error": str(e)}
