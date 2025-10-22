import os
from subprocess import CompletedProcess


def run_python_file(working_directory, file_path: str, args=[]):
    """Run a Python file located at file_path within the specified working_directory."""
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    # os.path.commonpath([abs_working_directory, abs_file_path])
    if not abs_file_path.startswith(abs_working_directory + os.sep) and abs_file_path != abs_working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found'
    if not os.path.splitext(file_path)[1] == ".py":
        return f'Error: File "{file_path}" is not a Python file.'
    try:
        import subprocess
        result: CompletedProcess[str] = subprocess.run(
            ["python3", abs_file_path] + args,
            cwd=abs_working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:            
            return f'STDERR: {result.stderr.strip()}'

        return f'STDOUT: {result.stdout.strip()}'
    except Exception as e:
        return f'Error: executing python file: {e}'