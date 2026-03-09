import os

import config


def get_file_content(working_dir, file_path):
    content = ""
    try:
        abs_working_dir = os.path.abspath(working_dir)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_target_dir = (
            os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
        )

        if not valid_target_dir:
            return (
                f'Error: Cannot read "{file_path}" as it is outside the permitted '
                "working directory"
            )
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            content = f.read(config.MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"
