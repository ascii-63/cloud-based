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
    try:
        files_in_directory = os.listdir(_directory)
    except Exception as e:
        print(f"Some error: {e}")
        return False

    for obj in files_in_directory:
        print(obj)

    # Check if the file is in the list
    if _file_name in files_in_directory:
        return True
    else:
        return False


if searchFileInDirectory("/home/pino/fake-data/images", "2023-12-09T08:53:25.144Z.jpg"):
    print("True")
else:
    print("False")
