from functions.get_files_info import get_file_content, get_files_info, run_python_file, write_file

result1 = run_python_file("calculator", "main.py")
print(result1)

result2 = run_python_file("calculator", "tests.py")
print(result2)

result3 = run_python_file("calculator", "../main.py")
print(result3)

result4 = run_python_file("calculator", "nonexistent.py")
print(result4)

result5 = run_python_file("calculator", "lorem.txt")
print(result5)