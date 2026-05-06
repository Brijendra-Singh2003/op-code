import os
import subprocess
import tempfile

from .result import err, ok

file_edit_tool = {
    "type": "function",
    "function": {
        "name": "file_edit",
        "description": "Applies a git-style unified diff patch to a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to patch.",
                },
                "patch": {
                    "type": "string",
                    "description": "The unified diff patch content.",
                },
            },
            "required": ["file_path", "patch"],
        },
    },
}


def file_edit_impl(file_path: str, patch: str) -> dict:
    print(f"\n[confirm] apply_patch(file_path={file_path!r})")
    if input("Allow? [y/N] ").strip().lower() != "y":
        return err("user denied permission").to_dict()
    patch_file = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".patch") as f:
            f.write(patch)
            patch_file = f.name
        result = subprocess.run(
            ["patch", file_path, patch_file], capture_output=True, text=True
        )
        if result.returncode != 0:
            return err(result.stderr or result.stdout).to_dict()
        return ok(file_path).to_dict()
    except Exception as e:
        return err(str(e)).to_dict()
    finally:
        if patch_file and os.path.exists(patch_file):
            os.unlink(patch_file)
