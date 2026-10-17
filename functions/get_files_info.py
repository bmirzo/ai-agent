import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'
        else: 
            try:
                nmd = {}
                names = os.listdir(target_dir)
                for name in names:
                    path = os.path.join(target_dir, name)
                    size = os.path.getsize(path)
                    is_dir = os.path.isdir(path)
                    nmd[name] = [size, is_dir]

                if directory == ".":
                    output = "Result for current directory:\n"
                else:
                    output = f"Result for '{directory}' directory:\n"

                for key, value in nmd.items():
                    output += f"- {key}: file_size={value[0]} bytes, is_dir={value[1]}\n"
                output = output.rstrip('\n')
                return output.rstrip("\n")
            except:
                return "Error: cannot find the files."
    except:
        return "Error: cannot verify the given directory."


