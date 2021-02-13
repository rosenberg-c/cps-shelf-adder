import sys


def open_csv(csv_path):
    if sys.version_info.major >= 3:
        return open(csv_path, newline='', )
    return open(csv_path)
