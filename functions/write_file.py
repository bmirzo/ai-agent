import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes the content to the specified file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": ("The path of the file to write to, relative to "
                        "the working directory."
                    ),
                },
                "content": {
                    "type": "string",
                    "description": "Content to write",
                },
            },
        },
         "required": ["file_path"],
            "additionalProperties": False,
    },
    "strict": True,
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Check whether the file path is inside the working directory
        valid_target = (
            os.path.commonpath([working_dir_abs, target_file])
            == working_dir_abs
        )

        if not valid_target:
            return (
                f'Error: Cannot write to "{file_path}" as it is outside '
                f'the permitted working directory'
            )

        # Check whether the target is an existing directory
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Create any missing parent directories
        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)

        # Write the content to the file
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" '
            f'({len(content)} characters written)'
        )

    except (OSError, ValueError) as e:
        return f"Error: {e}"