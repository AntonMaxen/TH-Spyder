from dotenv import load_dotenv
import os
import re

from session import Session
from page import Page

LOGIN_URL = "https://yh.pingpong.se/login/processlogin?disco=local"
BASE_URL = "https://yh.pingpong.se"

load_dotenv()

USERNAME = os.getenv('PP_USERNAME')
PASSWORD = os.getenv('PP_PASSWORD')

def create_payload():
    un_name = "login"
    pa_name = "password"
    payload = {
        un_name: USERNAME,
        pa_name: PASSWORD
    }
    return payload


def main():
    mySession = Session(True)
    payload = create_payload()
    cookie_name = "PPLoggedIn"
    mySession.login(LOGIN_URL, payload, cookie_name)
    print(f'is logged in {mySession._isloggedin}')
    filename = mySession.request_page(BASE_URL)
    print(filename)

    myPage = Page()
    myPage.load(filename)
    links = myPage.attributes([["a"]], "href")
    idlinks = [link for link in links if re.search("\/launchCourse.do\?id=\d", link)]
    ids = [re.sub("([^\d])", "", link) for link in idlinks]
    print(idlinks)
    print(ids)


    testfile = mySession.request_page(BASE_URL + "/launchCourse.do?id=603", "test_")
    newPage = Page()
    newPage.load(testfile)
    attr_list = newPage.attributes([["iframe"]], "src")
    contentlink = attr_list[0]

    next_page = mySession.request_page(BASE_URL + contentlink, "next_")
    newPage.load(next_page)
    text_list = newPage.text([["body"]])
    print("\n".join(text_list))


if __name__ == '__main__':
    main()
