import os

from .result import err, ok

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
            "required": ["file_name"],
        },
    },
}


def file_write_impl(file_name: str, folder_path: str = ".", content: str = "") -> dict:
    print(
        f"\n[confirm] create_n_write_file(file_name={file_name!r}, folder_path={folder_path!r})"
    )
    if input("Allow? [y/N] ").strip().lower() != "y":
        return err("user denied permission").to_dict()
    try:
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            return err(f"file already exists: {file_path}").to_dict()
        with open(file_path, "w") as f:
            f.write(content)
        return ok(file_path).to_dict()
    except Exception as e:
        return err(str(e)).to_dict()
