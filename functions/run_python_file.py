import os
import subprocess

from google.genai import types


def run_python_file(working_dir, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_dir)
        target = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_target_dir = (
            os.path.commonpath([abs_working_dir, target]) == abs_working_dir
        )

        if not valid_target_dir:
            return (
                f'Error: Cannot execute "{file_path}" as it is outside the permitted '
                "working directory"
            )
        if not os.path.isfile(target):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target]

        if args:
            command.append(args)

        completed_proc = subprocess.run(
            args=command,
            cwd=abs_working_dir,
            text=True,
            timeout=30,
            capture_output=True,
        )

        rvalue = ""

        if not completed_proc.returncode == 0:
            rvalue += f"Process exited with code {completed_proc.returncode} \n"
        if not completed_proc.stderr and not completed_proc.stdout:
            rvalue += "No output produced \n"

        rvalue += (
            f"STDOUT: {completed_proc.stdout} \n STDERR: {completed_proc.stderr} \n"
        )
        return rvalue

    except Exception as e:
        return f"Error: executing python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory with an optional argument string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional argument string to pass to the Python file",
            ),
        },
    ),
)
