import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None) -> str:

    # Always resolve working_directory as absolute
    abs_working_directory = os.path.abspath(working_directory)
    print(f"Working directory: {abs_working_directory}")

    # If directory is None or '.', use working_directory
    if directory is None or directory == ".":
        abs_directory = abs_working_directory
    # If directory is an absolute path, immediately reject as outside working_directory
    elif os.path.isabs(directory):
        print(f"Directory to list: {directory} (absolute path, rejected)")
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        abs_directory = os.path.abspath(os.path.join(abs_working_directory, directory))
    print(f"Directory to list: {abs_directory}")

    # os.chdir(abs_working_directory)

    # check if the directory is within the working directory
    if not os.path.commonpath([abs_directory, abs_working_directory]) == abs_working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # if directory is not a real directory, return an error
    if directory and not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'

    files_info = []
    for root, dirs, files in os.walk(abs_directory):
        # Calculate the relative path from abs_directory to current root
        rel_root = os.path.relpath(root, abs_directory)
        if rel_root == ".":
            rel_root = ""
        
        # Add directories
        for dirname in dirs:
            # Include relative path in the name
            if rel_root:
                dir_rel_path = os.path.join(rel_root, dirname)
            else:
                dir_rel_path = dirname
            file_info = {
                "name": dir_rel_path,
                "size": 0,  # Directories don't have a meaningful size
                "is_directory": True,
            }
            files_info.append(file_info)
        
        # Add files
        for filename in files:
            file_path = os.path.join(root, filename)
            # Include relative path in the name
            if rel_root:
                file_rel_path = os.path.join(rel_root, filename)
            else:
                file_rel_path = filename
            file_info = {
                "name": file_rel_path,
                "size": os.path.getsize(file_path),
                "is_directory": False,
            }
            files_info.append(file_info)

    # iterate through files_info and return a string in the format expected by tests:
    # "filename: file_size=X bytes, is_dir=True/False"
    files_info_str = []
    for file_info in files_info:
        file_str = f'{file_info["name"]}: file_size={file_info["size"]} bytes, is_dir={file_info["is_directory"]}'
        files_info_str.append(file_str)

    # Reset to the original working directory
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    return "\n".join(files_info_str)


if __name__ == "__main__":
    print("testing Calculator folder")
    print(get_files_info("calculator", "."))

    print("testing pkg folder")
    print(get_files_info("calculator", "pkg"))
