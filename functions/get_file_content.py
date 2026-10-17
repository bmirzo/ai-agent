import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets the content of the file specified file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": ("The path of the file to read, relative to "
                        "the working directory."
                    ),
                },
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Validate that the file is inside the working directory
        valid_target = (
            os.path.commonpath([working_dir_abs, target_file])
            == working_dir_abs
        )

        if not valid_target:
            return (
                f'Error: Cannot read "{file_path}" as it is outside '
                f'the permitted working directory'
            )

        # Check that the target is a regular file
        if not os.path.isfile(target_file):
            return (
                f'Error: File not found or is not a regular file: '
                f'"{file_path}"'
            )

        # Read up to MAX_CHARS and check whether more content exists
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += (
                    f'\n[...File "{file_path}" truncated at '
                    f'{MAX_CHARS} characters]'
                )

        return content

    except (OSError, ValueError, UnicodeError) as e:
        return f"Error: {e}"