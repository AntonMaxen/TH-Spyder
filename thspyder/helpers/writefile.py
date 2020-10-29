import os
from pathlib import Path
from thspyder.helpers.helper import get_project_root
import thspyder.helpers.myconstants as constants


def write_file(content, rel_path, filename):
    root = get_project_root()
    parent_dir = os.path.normpath(root)

    path = os.path.join(parent_dir, constants.STORAGE_FOLDER, constants.DATA_FOLDER, *rel_path)
    fullpath = os.path.join(path, filename)

    Path(path).mkdir(parents=True, exist_ok=True)

    with open(fullpath, 'w', encoding='utf8') as my_file:
        for line in content:
            my_file.write(line)
            my_file.write('\n')
        my_file.close()
