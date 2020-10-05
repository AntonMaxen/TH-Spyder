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

    myPage = Page()
    myPage.load(filename)
    links = myPage.attributes([["a"]], "href")
    idlinks = [link for link in links if re.search("\/launchCourse.do\?id=\d", link)]
    ids = [re.sub("([^\d])", "", link) for link in idlinks]
    print("\n".join(ids))

    testfile = mySession.request_page(BASE_URL + "/launchCourse.do?id=12051")
    newPage = Page()
    newPage.load(testfile)
    attr_list = newPage.attributes([["iframe"]], "src")
    contentlink = attr_list[0]

    next_page = mySession.request_page(BASE_URL + contentlink)
    newPage.load(next_page)
    print("\n".join(newPage.text([["body"]])))

    new_session = Session(False)
    wiki_path = new_session.request_page("https://en.wikipedia.org/wiki/Special:Random")
    wiki_page = Page()
    wiki_page.load(wiki_path)
    wiki_attr = wiki_page.attributes([["a"]], "href")
    #print("\n".join([attr for attr in wiki_attr if "cass" in attr]))
    print("\n".join(wiki_attr))


if __name__ == '__main__':
    main()
