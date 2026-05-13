file_read_tool = {
    "type": "function",
    "function": {
        "name": "file_read",
        "description": "Reads a file. Supports optional line range.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to read.",
                },
                "offset": {
                    "type": "integer",
                    "description": "Lines to skip from start. Defaults to 0",
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of lines to read. Reads till EOF if no value provided.",
                },
            },
            "required": ["file_path"],
        },
    },
}


def file_read_impl(
    file_path: str, offset: int | None = None, limit: int | None = None
) -> dict:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total = len(lines)
        if offset is None and limit is None:
            numbered = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
            return {"success": True, "data": "".join(numbered)}

        start = min(max(offset or 0, 0), total)
        end = min(start + limit if limit else total, total)
        selected = lines[start:end]
        numbered = [f"{i + start + 1}: {line}" for i, line in enumerate(selected)]
        return {"success": True, "data": "".join(numbered)}
    except Exception as e:
        return {"success": False, "error": str(e)}
