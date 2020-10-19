import requests
import os
import pickle
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse
import time

# project imports
from thspyder.helpers.helper import random_ua

load_dotenv()
USERNAME = os.getenv('PP_USERNAME')
PASSWORD = os.getenv('PP_PASSWORD')

SOURCE_URL = "https://yh.pingpong.se/courseId/11264/content.do?id=4744630"
True_URL = "https://yh.pingpong.se/pp/courses/course11264/published/1601480920383/resourceId/4879393/content/5e4540d8-7a81-4bb2-afc7-c4de59000348/5e4540d8-7a81-4bb2-afc7-c4de59000348.html"
BASE_URL = "https://yh.pingpong.se"
PPF_DATA = "/pp/courses/course11264/published/1601480920383/resourceId/4879393/content/5e4540d8-7a81-4bb2-afc7-c4de59000348/5e4540d8-7a81-4bb2-afc7-c4de59000348.html"
LOGIN_URL = "https://yh.pingpong.se/login/processlogin?disco=local"


class Session:
    def __init__(self, require_login=False):
        self._session = requests.session()
        self.set_headers()
        self._requirelogin = require_login
        self._isloggedin = False
        # not used yet
        self._baseurl = BASE_URL

    def set_headers(self, *args, **kwargs):
        if 'ua' in kwargs:
            ua = kwargs.get('ua')
            print("inside")
        else:
            ua = random_ua()
        self._session.headers.update({'user-agent': ua})

    def login(self, login_url, payload, cookie_name=None):
        login_result = self._session.post(login_url, data=payload, headers=dict(referer=login_url))

        # Some better error handling to check if user login is success or not TODO
        if login_result.ok:
            print("ok")
            # checking for cookie name if it exists the user is probably logged in
            if cookie_name is not None:
                good_cookie = len([cookie for cookie in self._session.cookies if cookie.name == cookie_name]) > 0
            else:
                good_cookie = True

            if good_cookie:
                self._isloggedin = True
                return self._isloggedin
            else:
                self._isloggedin = False
                return self._isloggedin
        else:
            print(f'Something went wrong, statuscode {login_result.status_code}')
            return False

    def request_page(self, url):
        # checking if logged in if required.
        if self._requirelogin and not self._isloggedin:
            print("you are not logged in")
            return False

        #Validate the request TODO make function for that
        valid_request = False
        tries = 0

        while not valid_request and tries < 3:
            result = self._session.get(url, headers=dict(referer=url))
            if result.status_code == 200:
                valid_request = True
            else:
                tries += 1
                print(f'Something went wrong with the status code {result.status_code} restarting the request with some delay.')
                time.sleep(2)

        # if valid then save page
        if valid_request:
            uri = urlparse(result.url)
            filename = os.path.basename(uri.path) + ".pickle"
            path = f'pages/{uri.netloc}{os.path.dirname(uri.path)}'
            fullpath = f'{path}/{filename}'

            Path(path).mkdir(parents=True, exist_ok=True)
            with open(fullpath, 'wb+') as p_file:
                pickle.dump(result, p_file)
            return fullpath
        else:
            return False

    def build_url(self, route):
        return self._baseurl + route


def main():
    pass


if __name__ == '__main__':
    main()
