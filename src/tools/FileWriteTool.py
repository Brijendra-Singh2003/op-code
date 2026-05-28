import os

from langchain_core.tools import tool


@tool
def file_write(file_path: str, content: str = "") -> dict:
    """
    Create a file at the specified path and write content to it.

    Args:
        file_path: Relative or absolute path to the file, e.g. './README.md' or 'src/utils.py'.
        content: Content to write to the file.

    Returns:
        A dictionary containing the operation result.
    """
    print(f"\n[confirm] file_write(file_path={file_path!r})")

    if input("Allow? [y/N] ").strip().lower() != "y":
        return {
            "success": False,
            "error": "user denied permission",
        }

    try:
        os.makedirs(
            os.path.dirname(file_path) or ".",
            exist_ok=True,
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "data": file_path,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
