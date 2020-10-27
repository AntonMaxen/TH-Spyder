from thspyder.helpers.helper import get_project_root
import thspyder.helpers.myconstants as constants
import os

TIMESTAMP = "timestamp"
FOLDERS = "folders"


class FileProcessor:
    def __init__(self, data_path, spider_name):
        self.data_path = os.path.join(get_project_root(), *data_path)
        self.spider_name = spider_name

    @property
    def full_path(self):
        return os.path.join(self.data_path, self.spider_name)

    def recent(self, amount=1):
        dirs = os.listdir(self.full_path)
        if amount > len(dirs):
            # raise Exception("Not enough folders to grab")
            amount = len(dirs)
            pass

        sorted_dirs = sorted(dirs, reverse=True)
        # returns Newest -> Oldest
        return [sorted_dirs[i] for i in range(amount)]

    def file_dicts(self, amount=2):
        last_two = self.recent(amount)
        file_dicts = []
        for timestamp in last_two:
            file_dict = {TIMESTAMP: timestamp, FOLDERS: []}
            path = os.path.join(self.full_path, timestamp)
            for root, dirs, files in os.walk(path):
                if len(files) > 0:
                    foldername = os.path.split(root)[-1]
                    file_dict[FOLDERS].append({
                        'name': foldername,
                        'root': root,
                        'files': files,
                        'filepaths': {f: os.path.join(root, f) for f in files}
                    })
            file_dicts.append(file_dict)

        return file_dicts

    def file_diff_recent(self):
        list_dicts = self.file_dicts()
        diff_dict = difference(list_dicts)
        return diff_dict


def difference(list_dict):
    diff_dict = {}
    if len(list_dict) < 2:
        for folder in list_dict[0][FOLDERS]:
            temp_dict = {}
            name = folder['name']
            for filename, path in folder['filepaths'].items():
                content = read_file(path)
                temp_dict[filename] = content
            diff_dict[name] = temp_dict
        return diff_dict

    dict_one = list_dict[0]
    dict_two = list_dict[1]
    for cat_one in dict_one[FOLDERS]:
        for cat_two in dict_two[FOLDERS]:
            if cat_one['name'] == cat_two['name']:
                name = cat_one['name']
                temp_dict = {}
                for filename_one, path_one in cat_one["filepaths"].items():
                    for filename_two, path_two in cat_two["filepaths"].items():
                        if filename_one == filename_two:
                            filename = filename_one
                            content_one = read_file(path_one)
                            content_two = read_file(path_two)

                            if dict_one[TIMESTAMP] > dict_two[TIMESTAMP]:
                                new_list = content_one
                                old_list = content_two
                            else:
                                new_list = content_two
                                old_list = content_one

                            temp_dict[filename] = list_difference(new_list, old_list)
                diff_dict[name] = temp_dict
    return diff_dict


def read_file(fullpath):
    with open(fullpath, encoding="utf8") as file:
        content = file.read().splitlines()

    return content


def list_difference(new_list, old_list):
    diff = []
    for item in new_list:
        if item not in old_list:
            diff.append(item)
    return diff


def main():
    processor = FileProcessor((constants.STORAGE_FOLDER, constants.DATA_FOLDER), "runescape")
    diff_dict = processor.file_diff_recent()

    for d, f in diff_dict.items():
        print(d)
        print(f)


if __name__ == '__main__':
    main()
