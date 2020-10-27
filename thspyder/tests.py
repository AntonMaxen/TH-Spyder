from dotenv import load_dotenv
import os

# project imports
from thspyder.helpers.listf import print_list, filter_list, trim_list, remove_duplicates, extract_list
from thspyder.session import Session
from thspyder.page import Page
from thspyder.helpers.utils import create_payload, visualize_page_text

LOGIN_URL = "https://yh.pingpong.se/login/processlogin?disco=local"
BASE_URL = "https://yh.pingpong.se"

load_dotenv()

USERNAME = os.getenv('PP_USERNAME')
PASSWORD = os.getenv('PP_PASSWORD')
FA_USERNAME = os.getenv('FA_USERNAME')
FA_PASSWORD = os.getenv('FA_PASSWORD')


def pingpong_test():
    # Start session and build login payload
    session = Session(True)
    post_url, payload = create_payload(LOGIN_URL, USERNAME, PASSWORD)
    cookie_name = "PPLoggedIn"
    session.login(post_url, payload, auth_func=lambda s: len([c for c in s.cookies if c.name == cookie_name]) > 0)
    print(f'is logged in {session.isloggedin}')

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
            attr_list = content_page.attributes([["iframe"]], ["src"])
            ppf_link = attr_list[0]

            ppf_page_path = session.request_page(BASE_URL + ppf_link)
            ppf_page = Page(ppf_page_path)
            print_list(ppf_page.get_text())

            print("*" * 30)

        print("-" * 20)


def wiki_test(n):
    # gets n number of wikipedia pages and prints all links on all of those pages
    new_session = Session(False)
    for _ in range(n):
        path = new_session.request_page("https://en.wikipedia.org/wiki/Special:Random")
        page = Page()
        page.load(path)
        print_list(page.get_links(["body"]))


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


def test_bs4():
    session = Session()
    page_path = session.request_page("https://en.wikipedia.org/wiki/Python_(programming_language)")
    page = Page(file=page_path)
    stripped_string = page.text(["body"], sep="|", strip=True)
    attributes = page.attributes([[True]], "src")
    print(attributes)


def main():
    pingpong_test()
    #wiki_test(20)
    #facebook_test()
    #test_bs4()


if __name__ == '__main__':
    main()
