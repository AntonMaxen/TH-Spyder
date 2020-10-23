import os
from pathlib import Path
from thspyder.helpers.helper import get_project_root


def get_file_content(fullpath):
    if os.path.isfile(fullpath):
        src_file = open(fullpath, 'r', encoding='utf8')
        content = src_file.read().splitlines()
        src_file.close()
    else:
        src_file = open(fullpath, 'x', encoding='utf8')
        content = []
        src_file.close()

    return content


def update_file(source, rel_path, filename):
    new_source = False
    root = get_project_root()
    parent_dir = os.path.normpath(root)

    path = os.path.join(parent_dir, "storage", "data", *rel_path)
    fullpath = os.path.join(path, filename)

    Path(path).mkdir(parents=True, exist_ok=True)
    content = get_file_content(fullpath)

    print(fullpath)

    if source not in content:
        new_source = True
        src_file = open(fullpath, 'a', encoding='utf8')
        src_file.write(source)
        src_file.write('\n')
        src_file.close()

    return new_source


def main():
    pass


if __name__ == '__main__':
    main()
