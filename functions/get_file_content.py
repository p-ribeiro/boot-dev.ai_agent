import os
from google.genai import types

MAX_CHARS = 10_000

def get_file_content(working_directory: str, file_path: str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory' 
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_file_path, "r") as f:
            file_content = f.read(MAX_CHARS + 1)
        
        if len(file_content) == MAX_CHARS + 1:
            return file_content[:MAX_CHARS] + f'\n[...File {file_path} truncated at {MAX_CHARS} characters]'
        else:
            return file_content
    except Exception as e:
        return f"Error reading file: {e}"

    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose contents should be read, relative to the working directory. ",
            ),
        },
        required=["file_path"]
    ),
)