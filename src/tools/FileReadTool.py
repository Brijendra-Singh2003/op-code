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
            "start_line": types.Schema(
                type=types.Type.INTEGER,
                description="Starting line number (1-based index)",
                default=1,
            ),
            "end_line": types.Schema(
                type=types.Type.INTEGER,
                description="Ending line number (inclusive). defaults to last line.",
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
    file_path: str, start_line: int | None = None, end_line: int | None = None
) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total_lines = len(lines)

        # Default behavior: return full file
        if start_line is None and end_line is None:
            numbered = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
            return "".join(numbered)

        # Normalize indices (convert to 0-based)
        start = max((start_line - 1) if start_line else 0, 0)
        end = end_line if end_line else total_lines

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
