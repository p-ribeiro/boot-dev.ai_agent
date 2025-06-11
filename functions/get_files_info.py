import os
import subprocess

MAX_CHARS = 10_000

def get_files_info(working_directory: str , directory: str = None) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir    
    
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory} as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: {directory} is not a directory'
    
    try:
        files_info = []
        for filename in os.listdir(target_dir):
            file_path = os.path.join(target_dir, filename)
            file_isdir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            files_info.append(f"- {filename}: file_size={file_size} bytes, is_dir={file_isdir}")
        return "\n".join(files_info)
        
    except Exception as e:
        return f"Error listing files: {e}"
        
    
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
        

def write_file(working_directory: str, file_path: str, content: str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory' 

    try:
        with open(abs_file_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

def run_python_file(working_directory: str, file_path: str) -> str:
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a python file.'
    
    try: 
        complete_process = subprocess.run(["python3", abs_file_path], timeout=30, capture_output=True, cwd=abs_working_directory)
    
        if complete_process.stdout.decode() == "" and complete_process.stderr.decode() == "":
            return "No output produced"
        
        result = [
            f"STDOUT: {complete_process.stdout.decode()}",
            f"STDERR: {complete_process.stderr.decode()}"
        ]
        
        if complete_process.returncode != 0:
            result.append(f"Process exited with code {complete_process.returncode}")
        
        return "\n".join(result)
    except Exception as e:
        return f'Error: executing Python file: {e}'
     
    
    
    
if __name__ == "__main__":
    ...