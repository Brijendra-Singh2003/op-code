from difflib import unified_diff
from pathlib import Path
from typing import Literal

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from tools.utils import request_approval

description = """Replace text in a file with optional occurrence validation.

- Try to keep `old_text` small, 2-3 lines from above and below may be enough.
- The tool first validates how many times `old_text` appears in the file. If `expected_occurrences` is provided and does not match the actual number of occurrences, the edit is aborted.
- Before applying any changes, a unified diff preview is displayed and the user must explicitly approve the edit.

Examples:
Replace a single occurrence:
    file_edit({
        file_path: "main.py",
        old_text: "DEBUG = True",
        new_text: "DEBUG = False",
    })

Replace all occurrences after validating there are exactly 3:
    file_edit({
        file_path: "config.py",
        old_text: "localhost",
        new_text: "db.internal",
        mode: "all",
        expected_occurrences: 3,
    })

Replace all occurrences without validating the count:
    file_edit({
        file_path: "config.py",
        old_text: "localhost",
        new_text: "db.internal",
        mode: "all",
        expected_occurrences: -1,
    })"""


class FileEditInput(BaseModel):
    file_path: str = Field(description="Path to the file to modify.")
    old_text: str = Field(description="Exact text to search for.")
    new_text: str = Field(description="Replacement text.")
    mode: Literal["first", "all"] = Field(
        default="first",
        description='Replacement mode.\n- "first": Replace only the first occurrence.\n- "all": Replace all occurrences.',
    )
    expected_occurrences: int = Field(
        default=1,
        description="Expected number of occurrences of `old_text` in the file.\n- Edit fails if `expected_occurrences` doesn't match actual occurrence count.\n- Pass -1 to disable occurrence validation.",
    )


@tool(description=description, args_schema=FileEditInput)
def file_edit(
    file_path: str,
    old_text: str,
    new_text: str,
    mode: Literal["first", "all"] = "first",
    expected_occurrences: int = 1,
) -> dict:
    try:
        path = Path(file_path)
        content = path.read_text()

        actual_occurrences = content.count(old_text)

        if actual_occurrences == 0:
            return {
                "success": False,
                "error": "no occurance of `old_text` found",
            }

        if expected_occurrences >= 0 and actual_occurrences != expected_occurrences:
            return {
                "success": False,
                "error": f"expected {expected_occurrences} occurrence(s), but found {actual_occurrences}",
            }

        if mode == "all":
            updated = content.replace(old_text, new_text)
            replacements = actual_occurrences
        else:
            updated = content.replace(old_text, new_text, 1)
            replacements = 1

        diff_lines = unified_diff(
            content.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile=f"{file_path} (before)",
            tofile=f"{file_path} (after)",
            lineterm="",
            n=3,
        )

        print("\n=== Proposed Changes ===\n")
        for line in diff_lines:
            if line.startswith("+") and not line.startswith("+++"):
                print(f"\033[32m{line}\033[0m", end="")
            elif line.startswith("-") and not line.startswith("---"):
                print(f"\033[31m{line}\033[0m", end="")
            else:
                print(line, end="")
        print("========== END ===========")

        rejection_message = request_approval(f"\nEditing file {file_path}")
        if rejection_message:
            return {
                "success": False,
                "error": f"user denied permission: {rejection_message}",
            }

        path.write_text(updated)

        return {
            "success": True,
            "data": {
                "file_path": file_path,
                "replacements": replacements,
                "occurrences_found": actual_occurrences,
            },
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
