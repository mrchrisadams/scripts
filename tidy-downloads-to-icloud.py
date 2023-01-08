import os
import pathlib
import shutil
from datetime import datetime


def tidy_new_downloads():
    """
    Return a lst of files in the folder to put into a new
    timestamped downloads directory
    """
    downloads_dir = pathlib.Path.home() / "Downloads"
    mess_dirs = set([file for file in downloads_dir.glob("Mess *")])
    download_files = set([file for file in downloads_dir.glob("*")])
    new_downloaded_files = download_files.difference(mess_dirs)

    today_date = datetime.now().date().strftime("%Y-%m-%d")
    today_dir = downloads_dir / f"Mess {today_date}"

    if not today_dir.exists():
        os.mkdir(today_dir)

    for file in new_downloaded_files:
        # only move files if they haven't already been moved
        dest_path = today_dir / file.name
        if not dest_path.exists():
            shutil.move(file, today_dir)


if __name__ == "__main__":
    tidy_new_downloads()
