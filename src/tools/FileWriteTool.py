import os

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from tools.utils import request_approval

description = """Writes content to a file on the local filesystem.

Usage:
- Parent directories will be created automatically if they do not exist.
- Existing files will be overwritten.
- User approval is asked by the tool before writing."""


class FileWriteInput(BaseModel):
    file_path: str = Field(description="Absolute path to the file to write")
    content: str = Field(description="Content to write to the file")


@tool(description=description, args_schema=FileWriteInput)
def file_write(
    file_path: str,
    content: str = "",
) -> dict:
    rejection_message = request_approval(f"Writing to file {file_path}\n")
    if rejection_message:
        return {
            "success": False,
            "error": f"user denied permission: {rejection_message}",
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
