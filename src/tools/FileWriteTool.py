import os

from google.genai import types

create_n_write_file = types.FunctionDeclaration(
    name="create_n_write_file",
    description="creates a file at a given location and returns its path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_name": types.Schema(
                type=types.Type.STRING,
                description="name of the file.",
            ),
            "folder_path": types.Schema(
                type=types.Type.STRING,
                description="path where to create the file",
                example="src/common",
                default=".",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to initialize file with",
                default="",
            ),
        },
        required=["file_name"],
    ),
    response=types.Schema(
        type=types.Type.STRING,
        description="path of the file created.",
    ),
)


def create_n_write_file_impl(
    file_name: str, folder_path: str = ".", content: str = ""
) -> str:
    try:
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, file_name)

        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(content)
        else:
            return f"error: File already exists: {file_path}"

        return file_path

    except Exception as e:
        return f"error: {str(e)}"
