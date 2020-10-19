from dotenv import load_dotenv
import os
from urllib.parse import urlparse

# project imports
from thspyder.helpers.listf import remove_junk, print_list, filter_list, trim_list, remove_duplicates, extract_list
from thspyder.session import Session
from thspyder.page import Page

LOGIN_URL = "https://yh.pingpong.se/login/processlogin?disco=local"
BASE_URL = "https://yh.pingpong.se"

load_dotenv()

USERNAME = os.getenv('PP_USERNAME')
PASSWORD = os.getenv('PP_PASSWORD')
FA_USERNAME = os.getenv('FA_USERNAME')
FA_PASSWORD = os.getenv('FA_PASSWORD')


def create_payload(form_url, username, password):
    # get login page and extract form hooks
    session = Session(False)
    login_page_path = session.request_page(form_url)
    login_page = Page(login_page_path)
    fields = login_page.login_fields()

    # edit data object with authentication
    payload = fields['data'].copy()
    payload[fields['un_name']] = username
    payload[fields['pa_name']] = password

    # handle post url
    base_url = 'https://' + urlparse(form_url).netloc
    action = fields['action']
    post_url = base_url + action if action else form_url
    return post_url, payload


def visualize_page_text(page_obj):
    # filter and print list of text from a page object
    page_obj.trim([["script"]])
    page_text_elements = page_obj.text_elements()
    page_text = remove_junk(page_text_elements)
    print_list(page_text)


def vizualize_page_links(page_obj):
    # print all links in page obj
    print_list(page_obj.attributes([["a"]], "href", outer_element="body"))


def pingpong_test():
    # Start session and build login payload
    session = Session(True)
    post_url, payload = create_payload(LOGIN_URL, USERNAME, PASSWORD)
    cookie_name = "PPLoggedIn"
    session.login(post_url, payload, cookie_name)
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
            active_text = content_page.text([["a", {"class": "active"}]])
            attr_list = content_page.attributes([["iframe"]], "src")
            ppf_link = attr_list[0]

            ppf_page_path = session.request_page(BASE_URL + ppf_link)
            ppf_page = Page(ppf_page_path)
            visualize_page_text(ppf_page)

            print("*" * 30)

        print("-" * 20)


def wiki_test(n):
    # gets n number of wikipedia pages and prints all links on all of those pages
    new_session = Session(False)
    for _ in range(n):
        path = new_session.request_page("https://en.wikipedia.org/wiki/Special:Random")
        page = Page()
        page.load(path)
        print_list(page.get_links())


def facebook_test():
    # facebook test with authentication, find a way to parse useful information TODO
    session = Session(False)
    session.set_headers()
    login_url = "https://m.facebook.com/login/?ref=dbl&fl"
    post_url, payload = create_payload(login_url, FA_USERNAME, FA_PASSWORD)
    session.login(post_url, payload)

    front_page_path = session.request_page("https://m.facebook.com/anton.maxen")
    front_page = Page(front_page_path)
    front_page.trim([["script"]])
    visualize_page_text(front_page)


def main():
    pingpong_test()
    #wiki_test(5)
    #facebook_test()


if __name__ == '__main__':
    main()
