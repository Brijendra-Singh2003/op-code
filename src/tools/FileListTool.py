import os

from langchain_core.tools import tool


@tool
def file_list(directory_path: str) -> dict:
    """
    Read and return a list of all folders and files present in a directory.

    Args:
        directory_path: Path of the directory to list.

    Returns:
        A dictionary containing the operation result.
    """
    print(f"Getting files in {directory_path}.")

    try:
        return {
            "success": True,
            "data": os.listdir(directory_path),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
