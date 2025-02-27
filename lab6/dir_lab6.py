import os
import shutil
import string

def list_items_in_path(path):
    # Task 1
    print("Directories:", [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
    print("Files:", [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    print("All items:", os.listdir(path))

def check_access(path):
    # Task 2
    print(f"Exists: {os.path.exists(path)}")
    print(f"Readable: {os.access(path, os.R_OK)}")
    print(f"Writable: {os.access(path, os.W_OK)}")
    print(f"Executable: {os.access(path, os.X_OK)}")

def test_path(path):
    # Task 3
    if os.path.exists(path):
        print(f"Directory: {os.path.dirname(path)}")
        print(f"Filename: {os.path.basename(path)}")
    else:
        print("Path does not exist.")

def count_lines_in_file(file_path):
    # Task 4
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print("Line count:", sum(1 for _ in file))
    except FileNotFoundError:
        print("File not found.")

def write_list_to_file(file_path, data):
    # Task 5
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines("\n".join(data))

def generate_text_files():
    # Task 6
    for letter in string.ascii_uppercase:
        with open(f"{letter}.txt", 'w') as file:
            file.write(f"This is file {letter}.txt")

def copy_file(src, dest):
    # Task 7
    try:
        shutil.copy(src, dest)
        print("File copied successfully.")
    except FileNotFoundError:
        print("Source file not found.")

def delete_file(path):
    # Task 8
    if os.path.exists(path) and os.access(path, os.W_OK):
        os.remove(path)
        print("File deleted.......")
    else:
        print("Cannot delete file: access denied or file does not exist.")
