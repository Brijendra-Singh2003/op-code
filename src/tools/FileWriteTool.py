import os

file_write_tool = {
    "type": "function",
    "function": {
        "name": "file_write",
        "description": "creates a file at a given location and returns its path.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Relative path to the file, e.g. './README.md' or 'src/utils.py'",
                },
                "content": {
                    "type": "string",
                    "description": "content to initialize file with",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}


def file_write_impl(file_path: str, content: str = "") -> dict:
    print(f"\n[confirm] file_write(file_path={file_path!r})")
    if input("Allow? [y/N] ").strip().lower() != "y":
        return {"success": False, "error": "user denied permission"}
    try:
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)
        return {"success": True, "data": file_path}
    except Exception as e:
        return {"success": False, "error": str(e)}
