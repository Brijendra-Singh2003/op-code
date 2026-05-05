import math

from google.genai import types

read_file = types.FunctionDeclaration(
    name="read_file",
    description="Reads a file. Supports optional line range.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to read.",
                example="src/main.py",
            ),
            "offset": types.Schema(
                type=types.Type.INTEGER,
                description="Lines to skip from start.",
                default=0,
            ),
            "limit": types.Schema(
                type=types.Type.INTEGER,
                description="Number of lines to read. Reade till EOF if not provided.",
            ),
        },
        required=["file_path"],
    ),
    response=types.Schema(
        type=types.Type.STRING,
        description="file content. Each line is prefixed with its 1-based line number (e.g. '12: code...') to enable precise edits.",
    ),
)


def read_file_impl(
    file_path: str, offset: int | None = None, limit: int | None = None
) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total_lines = len(lines)

        # Default behavior: return full file
        if offset is None and limit is None:
            numbered = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
            return "".join(numbered)

        start = max(offset if offset else 0, 0)
        end = start + limit if limit else total_lines

        # Clamp to file bounds
        start = min(start, total_lines)
        end = min(end, total_lines)

        if start > end:
            return "error: start_line cannot be greater than end_line"

        selected = lines[start:end]
        numbered = [f"{i + start + 1}: {line}" for i, line in enumerate(selected)]
        return "".join(numbered)

    except Exception as e:
        return f"error: {str(e)}"
