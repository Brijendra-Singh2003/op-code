import os

from langchain_core.tools import tool
from pydantic import BaseModel, Field

description = "Read and return a list of all folders and files present in a directory."


class FileListInput(BaseModel):
    directory_path: str = Field(description="Absolute path of the directory to list.")


@tool(description=description, args_schema=FileListInput)
def file_list(directory_path: str) -> dict:
    print(f"Getting files in {directory_path}")
    try:
        items = os.listdir(directory_path)

        for i in range(len(items)):
            full_path = os.path.join(directory_path, items[i])

            if os.path.isdir(full_path):
                items[i] += "/"

        return {
            "success": True,
            "data": items,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
