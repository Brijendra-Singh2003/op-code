import os

from langchain_core.tools import tool


@tool
def file_list(directory_path: str) -> dict:
    """Read and return a list of all folders and files present in a directory.

    Args:
        directory_path: Absolute path of the directory to list."""

    print(f"Getting files in {directory_path}")
    try:
        items = os.listdir(directory_path)

        for i in range(len(items)):
            full_path = os.path.join(directory_path, items[i])

            if os.path.isdir(full_path):
                items[i] += '/'

        return {
            "success": True,
            "data": items,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
