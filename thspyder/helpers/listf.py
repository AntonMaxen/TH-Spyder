import re


def print_list(my_list):
    print("\n".join([str(item) for item in my_list]))


def filter_list(my_list, pattern):
    return [item for item in my_list if re.search(pattern, item)]


def trim_list(my_list, pattern, separator=""):
    return [re.sub(pattern, separator, item) for item in my_list]


def extract_list(my_list, pattern):
    return [re.search(pattern, item)[0] for item in my_list]


def clean_list(my_list):
    return [item for item in my_list if item]


def strip_list(my_list):
    return [item.strip() for item in my_list]


def remove_duplicates(my_list):
    return list(set(my_list))


def remove_junk(my_list):
    return clean_list(trim_list(my_list, "\n|\\xa0"))


def replace_newlines(my_list):
    return strip_list(trim_list(my_list, '(\\n)+', " "))
