import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": (
            "Executes a Python file within the permitted working directory "
            "and returns its stdout, stderr, and exit code."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "The path to the Python file to execute, "
                        "relative to the working directory."
                    ),
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": (
                        "Optional list of command-line arguments "
                        "to pass to the Python script."
                    ),
                },
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Check that the file is inside the working directory
        valid_target = (
            os.path.commonpath([working_dir_abs, absolute_file_path])
            == working_dir_abs
        )

        if not valid_target:
            return (
                f'Error: Cannot execute "{file_path}" as it is outside '
                f'the permitted working directory'
            )

        # Check that the file exists and is a regular file
        if not os.path.isfile(absolute_file_path):
            return (
                f'Error: "{file_path}" does not exist or is not a regular file'
            )

        # Check that it is a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build the command
        command = ["python", absolute_file_path]

        if args:
            command.extend(args)

        # Execute the Python file
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Build the output
        output = []

        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")

        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output.append("No output produced")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
