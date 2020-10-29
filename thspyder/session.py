import os
import re
import pickle
import requests
from pathlib import Path
from urllib.parse import urlparse

# project imports
from thspyder.helpers.helper import random_ua, get_project_root
import thspyder.helpers.myconstants as constants


class Session:
    """Class Session is holding a session it makes requests with"""
    def __init__(self, require_login=False):
        self.session = requests.session()
        self.set_headers()
        self._requirelogin = require_login
        self.isloggedin = False

    def set_headers(self, **kwargs):
        """sets headers for main session"""
        if 'ua' in kwargs:
            ua = kwargs.get('ua')
        else:
            ua = random_ua()
        self.session.headers.update({'user-agent': ua})

    def login(self, login_url, payload, auth_func=None):
        """issues a post request with given payload and url,
        if auth function is given it will evalute if login
        is succesful or not"""
        login_result = self.session.post(login_url, data=payload, headers=dict(referer=login_url))

        # Some better error handling to check if user login is success or not TODO
        if login_result.ok:
            # checking for cookie name if it exists the user is probably logged in
            if isinstance(auth_func, str):
                auth_func = create_function_from_string(auth_func)

            if auth_func is not None:
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
        """issues a get request with given url and pickles the result"""
        # checking if logged in if required.
        if self._requirelogin and not self.isloggedin:
            raise Exception(f'Login required for that request')

        result = self.session.get(url, headers=dict(referer=url))
        if result.status_code == 200:
            return pickle_result(result)
        else:
            raise Exception(f'Request error code: {result.status_code}')


def pickle_result(result):
    """building filestructure from url and saves file in that structure"""
    path, fullpath = build_paths(result.url, "pickle")

    Path(path).mkdir(parents=True, exist_ok=True)
    with open(fullpath, 'wb+') as p_file:
        pickle.dump(result, p_file)

    return fullpath


def build_paths(url, file_suffix):
    """builds filestructure from url"""
    uri = urlparse(url)
    filename = f'{os.path.basename(uri.path)}.{file_suffix}'
    root = get_project_root()
    parent_dir = os.path.normpath(root)

    urlpath = os.path.dirname(uri.path)
    clean_urlpath = [p for p in re.split('(/+)', urlpath) if p and not re.match('(/+)', p)]

    path = os.path.join(parent_dir, constants.STORAGE_FOLDER, constants.PAGE_FOLDER, uri.netloc, *clean_urlpath)
    fullpath = os.path.join(path, filename)

    return path, fullpath


def create_function_from_string(string):
    """with a given string execute it as python function and return the function"""
    if string is None:
        return None

    if 'lambda' in string:
        string = f'func = {string}'
    loc = {}
    exec(string, {}, loc)
    funcs = [loc.get(func, None) for func in loc.keys()]
    return funcs[0] if len(funcs) > 0 else None
