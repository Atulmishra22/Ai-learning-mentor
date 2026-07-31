import os
from pathlib import Path

def check_files_exist(file_path: str) -> bool:
    """
    Check if the provided file path exists.

    Args:
        file_path (str): The path to the file to check.

    """
    
    path = Path(file_path)
    if not path.exists():
        
        return False
    elif not path.is_file():
        
        return False

    absolute_path = path.resolve()
    check_relative_path = absolute_path.is_relative_to(Path.cwd()) # Check if the file is within the current working directory
    if not check_relative_path:
        return False
    return True

def read_file(file_path: str) -> str:
    """
    Read the content of the provided file path.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The content of the file    .
    """
    path = Path(file_path)
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "this is not readable"

    return content
