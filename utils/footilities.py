import os
import datetime


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


def date_from_filename(filename: str) -> datetime.datetime:
    """
    Return datetime.datetime instance from any filename as
    tryydoyhhmmss.hld.root.root or styydoyhhmmss.hld.root.root

    :param filename: Filename like tryydoyhhmmss.hld.root.root or
        styydoyhhmmss.hld.root.root.
    :return: datetime.datetime obkect.
    """

    if not filename.startswith(("st", "tr")) or not filename.endswith(".hld.root.root"):
        raise Exception("Filename must be like tryydoyhhmmss.hld.root.root "
                        "or styydoyhhmmss.hld.root.root")

    yy = int(f"20{filename[2:4]}")
    doy = int(filename[4:7])
    hh = int(filename[7:9])
    mm = int(filename[9:11])
    ss = int(filename[11:13])

    return datetime.datetime.combine(
        datetime.date(yy, 1, 1) + datetime.timedelta(doy + 1),
        datetime.time(hour=hh, minute=mm, second=ss)
    )
