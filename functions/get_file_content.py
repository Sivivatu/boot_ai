import os
import config

from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    try:
        # Get absolute paths
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        # Check if file_path is outside the working_directory
        try:
            os.path.commonpath([abs_working_directory, abs_file_path])
            if not abs_file_path.startswith(abs_working_directory + os.sep) and abs_file_path != abs_working_directory:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        except ValueError:
            # Different drives on Windows or other issues
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if the file_path is not a file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Truncate if necessary
        if len(content) > config.FILE_LIMIT:
            return content[:config.FILE_LIMIT] + f'[...File "{file_path}" truncated at {config.FILE_LIMIT} characters]'
        
        return content
    
    except Exception as e:
        return f'Error: {str(e)}'

