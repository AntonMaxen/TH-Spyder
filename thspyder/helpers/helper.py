import random
import re
from pathlib import Path


def get_project_root():
    # Based of how deep this file is in the file structure, if moving files change this functions
    return Path(__file__).parent.parent.parent


def random_ua():
    ua_strings = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0.1; RedMi Note 5 Build/RB3N5C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36"
    ]
    return random.choice(ua_strings)


def add_prefix(str_list, prefix):
    return [prefix + s for s in str_list]


def reformat_youtube_embed(links):
    new_links = [link.replace('https://www.youtube.com/embed', 'https://youtu.be') for link in links]
    reformatted_links = [re.sub('(\\?ecver=\\d)', '', link) for link in new_links]
    return reformatted_links


def main():
    pass


if __name__ == '__main__':
    main()
