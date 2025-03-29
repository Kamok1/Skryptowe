import os
import sys
from env_vars import get_variable
from constans import PATH

def get_path_dirs():
    path_value = get_variable(PATH)
    return [p for p in path_value.split(os.pathsep) if p.strip()]

def get_executable_files(directory):
    try:
        files = os.listdir(directory)
        return [f for f in files if os.path.isfile(os.path.join(directory, f)) and os.access(os.path.join(directory, f), os.X_OK)]
    except FileNotFoundError:
        return []
    except PermissionError:
        return []

def list_path_dirs():
    path_dirs = get_path_dirs()
    for directory in path_dirs:
        print(directory)

def list_executables():
    for directory in get_path_dirs():
        print(f"\n[{directory}]")
        executables = get_executable_files(directory)
        if executables:
            print("\n".join(executables))
        else:
            print("No executable files found.")

if __name__ == "__main__":
    list_executables()
    if "--list" in sys.argv:
        list_path_dirs()
    if "--executables" in sys.argv:
        list_executables()
    else:
        print("python path_info.py [--list | --executables]")
