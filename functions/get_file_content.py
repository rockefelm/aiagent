import os
from functions.config import *

def get_file_content(working_directory, file_path):
    joined_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(joined_path)
    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(joined_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(joined_path, 'r') as file:
            content = file.read(MAX_CHARS)
            next_char = file.read(1)
            if next_char:
                content += '[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error: {str(e)}'