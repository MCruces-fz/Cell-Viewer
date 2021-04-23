import os


def basename(file_path: str, extension: bool = False):
    """
    Get the basename of the full path to the file.

    :param file_path: Full path to the file.
    :param extension: If returns filename with extension or not.
    """
    file_name = os.path.basename(file_path)
    if not extension:
        file_name, *_ = file_name.split(".")
    return file_name
