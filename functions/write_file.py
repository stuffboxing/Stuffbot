import os


def write_file(working_dir, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_dir)
        target = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_target_dir = (
            os.path.commonpath([abs_working_dir, target]) == abs_working_dir
        )

        if not valid_target_dir:
            return (
                f'Error: Cannot write to "{file_path}" as it is outside the permitted '
                "working directory"
            )
        if os.path.isdir(target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target), exist_ok=True)

        with open(target, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
