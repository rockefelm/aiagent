import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    absolute_path = os.path.abspath(full_path)
    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    try:
        lines = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            item_size = os.path.getsize(item_path)
            item_is_dir = os.path.isdir(item_path)
            lines.append(f"- {item}: file_size={item_size} bytes, is_dir={item_is_dir}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {str(e)}"