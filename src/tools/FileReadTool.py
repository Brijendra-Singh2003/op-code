from langchain_core.tools import tool
from pydantic import BaseModel, Field

MAX_LINES_TO_READ = 300

description = """Reads a file from the local filesystem. You can access any file directly by using this tool.
Assume this tool is able to read all files on the machine. If the User provides a path to a file assume that path is valid. It is okay to read a file that does not exist; an error will be returned.

Usage:
- The file_path parameter must be an absolute path, not a relative path."""


class FileReadInput(BaseModel):
    file_path: str = Field(description="Absolute path to the file to read")
    offset: int = Field(description="Line number to start reading from", default=0)
    limit: int = Field(
        description="Maximum number of lines to read", default=MAX_LINES_TO_READ
    )


@tool(description=description, args_schema=FileReadInput)
def file_read(
    file_path: str,
    offset: int = 0,
    limit: int = MAX_LINES_TO_READ,
) -> dict:
    print(f"Reading file {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total_lines = len(lines)
        start = min(max(offset, 0), total_lines)
        end = min(
            start + limit if limit is not None else total_lines,
            total_lines,
        )

        selected = lines[start:end]
        numbered = [f"{i + start + 1}: {line}" for i, line in enumerate(selected)]

        return {
            "success": True,
            "data": "".join(numbered),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


__all__ = ["file_read"]
