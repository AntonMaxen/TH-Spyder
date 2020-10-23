import requests
import os
import re
import pickle
from pathlib import Path
from urllib.parse import urlparse

# project imports
from thspyder.helpers.helper import random_ua, get_project_root


class Session:
    def __init__(self, require_login=False):
        self.session = requests.session()
        self.set_headers()
        self._requirelogin = require_login
        self.isloggedin = False

    def set_headers(self, *args, **kwargs):
        if 'ua' in kwargs:
            ua = kwargs.get('ua')
        else:
            ua = random_ua()
        self.session.headers.update({'user-agent': ua})

    def login(self, login_url, payload, auth_func=None):
        login_result = self.session.post(login_url, data=payload, headers=dict(referer=login_url))

        # Some better error handling to check if user login is success or not TODO
        if login_result.ok:
            # checking for cookie name if it exists the user is probably logged in
            if auth_func is not None:
                print(f"Using auth function: {auth_func}")
                if auth_func(self.session):
                    self.isloggedin = True
                else:
                    self.isloggedin = False

            else:
                print("WARN: no auth function given, gonna hope the request succeeded")
                self.isloggedin = True
        else:
            raise Exception(f'Something went wrong, statuscode {login_result.status_code}')

        return self.isloggedin

    def request_page(self, url):
        # checking if logged in if required.
        if self._requirelogin and not self.isloggedin:
            raise Exception(f'Login required for that request')

        result = self.session.get(url, headers=dict(referer=url))
        if result.status_code == 200:
            return pickle_result(result, "pages")
        else:
            raise Exception(f'Request error code: {result.status_code}')


def pickle_result(result, folder=""):
    path, fullpath = build_paths(result.url, folder, "pickle")

    Path(path).mkdir(parents=True, exist_ok=True)
    with open(fullpath, 'wb+') as p_file:
        pickle.dump(result, p_file)

    return fullpath


def build_paths(url, folder, file_suffix):
    uri = urlparse(url)
    filename = f'{os.path.basename(uri.path)}.{file_suffix}'
    root = get_project_root()
    parent_dir = os.path.normpath(root)

    urlpath = os.path.dirname(uri.path)
    clean_urlpath = [p for p in re.split('(/+)', urlpath) if p and not re.match('(/+)', p)]

    path = os.path.join(parent_dir, "storage", folder, uri.netloc, *clean_urlpath)
    fullpath = os.path.join(path, filename)
    print(fullpath)

    return path, fullpath


def main():
    session = Session()
    page_path = session.request_page("https://www.youtube.com")
    print(page_path)

    pass


if __name__ == '__main__':
    main()
