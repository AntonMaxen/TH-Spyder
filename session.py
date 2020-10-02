import requests
import os
import pickle
import time
from dotenv import load_dotenv
from urllib.parse import urlparse
load_dotenv()

USERNAME = os.getenv('PP_USERNAME')
PASSWORD = os.getenv('PP_PASSWORD')

LOGIN_URL = "https://yh.pingpong.se/login/processlogin?disco=local"
SOURCE_URL = "https://yh.pingpong.se/courseId/11264/content.do?id=4744630"
True_URL = "https://yh.pingpong.se/pp/courses/course11264/published/1601480920383/resourceId/4879393/content/5e4540d8-7a81-4bb2-afc7-c4de59000348/5e4540d8-7a81-4bb2-afc7-c4de59000348.html"
BASE_URL = "https://yh.pingpong.se"
PPF_DATA = "/pp/courses/course11264/published/1601480920383/resourceId/4879393/content/5e4540d8-7a81-4bb2-afc7-c4de59000348/5e4540d8-7a81-4bb2-afc7-c4de59000348.html"


class Session:
    def __init__(self):
        self._session = requests.session()
        self._requirelogin = True
        self._isloggedin = False
        self._baseurl = BASE_URL
        #self.model = model._model

    def login(self):
        # Function that gets name of payloadnames
        p_load_un_name = "login"
        p_load_pa_name = "password"
        payload = {
            p_load_un_name: USERNAME,
            p_load_pa_name: PASSWORD
        }
        login_result = self._session.post(LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))

        if login_result.status_code == 200:
            if login_result.url != LOGIN_URL:
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

        if valid_request:
            uri = urlparse(result.url)
            filename = uri.netloc + ".pickle"
            with open(filename, 'wb+') as p_file:
                pickle.dump(result, p_file)

            return filename
        else:
            return False

    def build_url(self, route):
        return self._baseurl + route


def main():
    my_session = Session()
    result = my_session.login()
    filename = my_session.request_page(SOURCE_URL)
    print(filename)
    pass


if __name__ == '__main__':
    main()
