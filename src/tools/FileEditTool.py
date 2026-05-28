import os
import subprocess
import tempfile

from langchain_core.tools import tool


@tool
def file_edit(file_path: str, patch: str) -> dict:
    """Apply a git-style unified diff patch to a file.

    Args:
        file_path: Path of the file to patch.
        patch: Git-style unified diff patch to apply.

    Returns:
        Result dictionary containing success status and data/error."""

    print(f"\n[confirm] apply_patch(file_path={file_path!r})")

    if input("Allow? [y/N] ").strip().lower() != "y":
        return {
            "success": False,
            "error": "user denied permission",
        }

    patch_file = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            mode="w",
            suffix=".patch",
        ) as f:
            f.write(patch)
            patch_file = f.name

        result = subprocess.run(
            ["patch", file_path, patch_file],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr or result.stdout,
            }

        return {
            "success": True,
            "data": file_path,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

    finally:
        if patch_file and os.path.exists(patch_file):
            os.unlink(patch_file)
