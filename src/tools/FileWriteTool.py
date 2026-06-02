import os

from langchain_core.tools import tool
from pydantic import BaseModel, Field


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
    print(f"Writing to file {file_path}\n")
    print(content)

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


__all__ = ["file_write"]
