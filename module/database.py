# database.py

import os


def searchFileInDirectory(_directory, _file_name):
    """
    Search for a file in a directory.

    Parameters:
    - _directory: The directory to search in.
    - _file_name: The name of the file to search for.

    Returns:
    - True if the file is found, False otherwise.
    """
    # Get the list of files in the directory
    files_in_directory = os.listdir(_directory)

    # Check if the file is in the list
    if _file_name in files_in_directory:
        return True
    else:
        return False
