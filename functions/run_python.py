import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    joined_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(joined_path)
    
    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(absolute_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(
            ['python', absolute_path] + args,
            check=True,
            timeout=30,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=working_directory
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"
    if (not completed_process.stdout.strip()) and (not completed_process.stderr.strip()):
        return "No output produced."

    output_parts = []
    if completed_process.stdout.strip():
        output_parts.append("STDOUT: " + completed_process.stdout)
    if completed_process.stderr.strip():
        output_parts.append("STDERR: " + completed_process.stderr)
    if completed_process.returncode != 0:
        output_parts.append(f"Process exited with code {completed_process.returncode}")
    return "\n".join(output_parts)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python",
    description="Runs a .py file constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
            ),
        },
        required=["file_path"],
    ),
)