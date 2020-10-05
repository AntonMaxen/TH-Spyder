from dotenv import load_dotenv
import os
import re
import random

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


def print_list(my_list):
    print("\n".join(my_list))


def pingpong_test():
    # Start session and build login payload
    session = Session(True)
    payload = create_payload()
    cookie_name = "PPLoggedIn"
    session.login(LOGIN_URL, payload, cookie_name)
    print(f'is logged in {session._isloggedin}')

    # parse the page to look for all course ids
    base_page_path = session.request_page(BASE_URL)
    base_page = Page(base_page_path)
    links = base_page.get_links()
    idlinks = [link for link in links if re.search("\/launchCourse.do\?id=\d", link)]
    ids = [re.sub("([^\d])", "", link) for link in idlinks]

    # use ids to start a new request
    ids = list(set(ids))
    for id in ids:
        course_page_path = session.request_page(BASE_URL + f'/launchCourse.do?id={id}')
        course_page = Page(course_page_path)
        attr_list = course_page.attributes([["iframe"]], "src")
        contentlink = attr_list[0]

        # use content link to get final page
        content_page_path = session.request_page(BASE_URL + contentlink)
        content_page = Page(content_page_path)
        print_list(content_page.get_text())
        print("")


def wiki_test():
    new_session = Session(False)
    path = new_session.request_page("https://en.wikipedia.org/wiki/Special:Random")
    page = Page()
    page.load(path)
    print_list(page.get_links())


def main():
    pingpong_test()


if __name__ == '__main__':
    main()
