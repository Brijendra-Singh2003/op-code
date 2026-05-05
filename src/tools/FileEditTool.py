import subprocess
import tempfile

from google.genai import types

apply_patch = types.FunctionDeclaration(
    name="apply_patch",
    description="Applies a git-style unified diff patch to a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to read.",
                example="src/main.py",
            ),
            "patch": types.Schema(
                type=types.Type.STRING,
            ),
        },
        required=["file_path", "patch"],
    ),
    response=types.Schema(
        type=types.Type.STRING,
        description="path of the file edited.",
    ),
)


def apply_patch_impl(file_path: str, patch: str) -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
            f.write(patch)
            patch_file = f.name

        result = subprocess.run(
            ["patch", file_path, patch_file],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return f"error: {result.stderr or result.stdout}"

        return file_path

    except Exception as e:
        return f"error: {str(e)}"
