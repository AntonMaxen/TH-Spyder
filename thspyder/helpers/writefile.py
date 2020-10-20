import os
from pathlib import Path


def get_file_content(fullpath, filename):
    if os.path.isfile(f'./{fullpath}'):
        src_file = open(f'{fullpath}', 'r', encoding='utf-8')
        content = src_file.read().splitlines()
        src_file.close()
    else:
        print("hello")
        src_file = open(f'{fullpath}', 'x', encoding='utf-8')
        print(src_file)
        print(f'Created file: {src_file}')
        content = []
        src_file.close()

    return content


def update_file(source, rel_path, filename):
    new_source = False

    path = f'data/{rel_path}'
    fullpath = f'{path}/{filename}'
    Path(path).mkdir(parents=True, exist_ok=True)
    content = get_file_content(fullpath, filename)

    if source not in content:
        new_source = True
        src_file = open(f'{fullpath}', 'a', encoding='utf-8')
        src_file.write(source)
        src_file.write('\n')
        src_file.close()

    return new_source


def main():
    pass


if __name__ == '__main__':
    main()
