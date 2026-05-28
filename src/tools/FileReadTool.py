from langchain_core.tools import tool


@tool
def file_read(
    file_path: str,
    offset: int = 0,
    limit: int | None = None,
) -> dict:
    """
    Read a file with optional line range support.

    Args:
        file_path: Path of the file to read.
        offset: Number of lines to skip from the start. Defaults to 0.
        limit: Number of lines to read. Reads until EOF if not provided.

    Returns:
        A dictionary containing the operation result.
    """
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
