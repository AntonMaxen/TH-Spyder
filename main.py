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
FA_USERNAME = os.getenv('FA_USERNAME')
FA_PASSWORD = os.getenv('FA_PASSWORD')


def create_payload(un_name, pa_name, username, password):
    payload = {
        un_name: username,
        pa_name: password
    }
    return payload


def print_list(my_list):
    print("\n".join([str(item) for item in my_list]))


def filter_list(my_list, pattern):
    return [item for item in my_list if re.search(pattern, item)]


def trim_list(my_list, pattern):
    return [re.sub(pattern, "", item) for item in my_list]


def extract_list(my_list, pattern):
    return [re.search(pattern, item)[0] for item in my_list]


def clean_list(my_list):
    return [item for item in my_list if item]


def remove_duplicates(my_list):
    return list(set(my_list))


def remove_junk(my_list):
    return clean_list(trim_list(my_list, "\n|\\xa0"))


def visualize_page_text(page_obj):
    page_obj.trim([["script"]])
    page_text_elements = page_obj.text_elements()
    page_text = remove_junk(page_text_elements)
    return page_text


def vizualize_page_links(page_obj):
    print(page_obj.page.title)
    print_list(page_obj.attributes([["a"]], "href", outer_element="body"))


def pingpong_test():
    # Start session and build login payload
    session = Session(True)
    payload = create_payload("login", "password", USERNAME, PASSWORD)
    cookie_name = "PPLoggedIn"
    session.login(LOGIN_URL, payload, cookie_name)
    print(f'is logged in {session._isloggedin}')

    # parse the page to look for all course ids
    base_page_path = session.request_page(BASE_URL)
    base_page = Page(base_page_path)
    links = base_page.get_links()
    idlinks = filter_list(links, "\/launchCourse.do\?id=\d")
    ids = trim_list(idlinks, "([^\d])")

    # use ids to start a new request
    ids = remove_duplicates(ids)
    for id in ids:
        course_page_path = session.request_page(BASE_URL + f'/launchCourse.do?id={id}')
        course_page = Page(course_page_path)
        course_links = course_page.get_links(("div", {"id": "courseMainBox"}))
        filtered_course_links = filter_list(course_links, "\/content.do\?id=\d")
        course_ids = extract_list(filtered_course_links, "id=(\d)*")
        course_ids = remove_duplicates(course_ids)
        course_ids = trim_list(course_ids, "([^\d])")

        for course_id in course_ids:
            content_page_path = session.request_page(BASE_URL + f'/courseId/{id}/content.do?id={course_id}')
            content_page = Page(content_page_path)
            #print("\n".join([item.text for item in content_page.elements((("a", {"class": "active"})))]))
            active_text = content_page.text([["a", {"class": "active"}]])
            attr_list = content_page.attributes([["iframe"]], "src")
            ppf_link = attr_list[0]

            ppf_page_path = session.request_page(BASE_URL + ppf_link)
            ppf_page = Page(ppf_page_path)
            text = visualize_page_text(ppf_page)
            print_list(text)

            print("*" * 30)

        print("-" * 20)


def wiki_test():
    new_session = Session(False)
    for _ in range(30):
        path = new_session.request_page("https://en.wikipedia.org/wiki/Special:Random")
        page = Page()
        page.load(path)
        print_list(page.get_links())


def login_fields(form_url):
    session = Session(False)
    path = session.request_page(form_url)
    page = Page(path)
    fields = page.login_fields()
    action = fields['action']
    un_name = fields['un_name']
    pa_name = fields['pa_name']
    payload = create_payload(un_name, pa_name, FA_USERNAME, FA_PASSWORD)
    session.login(BASE_URL + action, payload)


def main():
    form_url = "https://www.facebook.com"
    # pingpong_test()
    # wiki_test()
    login_fields(form_url)


if __name__ == '__main__':
    main()
