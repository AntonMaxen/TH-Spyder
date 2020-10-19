from dotenv import load_dotenv
import os

# project imports
from thspyder.helpers import listf
from thspyder.session import Session
from thspyder.page import Page

LOGIN_URL = "https://yh.pingpong.se/login/processlogin?disco=local"
BASE_URL = "https://yh.pingpong.se"

load_dotenv()

USERNAME = os.getenv('PP_USERNAME')
PASSWORD = os.getenv('PP_PASSWORD')
FA_USERNAME = os.getenv('FA_USERNAME')
FA_PASSWORD = os.getenv('FA_PASSWORD')


def create_payload(form_url, base_url, username, password):
    session = Session(False)
    login_page_path = session.request_page(form_url)
    login_page = Page(login_page_path)
    fields = login_page.login_fields()

    action = fields['action']
    payload = fields['data'].copy()
    payload[fields['un_name']] = username
    payload[fields['pa_name']] = password
    post_url = base_url + action if action else form_url
    return post_url, payload


def visualize_page_text(page_obj):
    page_obj.trim([["script"]])
    page_text_elements = page_obj.text_elements()
    page_text = listf.remove_junk(page_text_elements)
    return page_text


def vizualize_page_links(page_obj):
    print(page_obj.page.title)
    listf.print_list(page_obj.attributes([["a"]], "href", outer_element="body"))


def pingpong_test():
    # Start session and build login payload
    session = Session(True)
    post_url, payload = create_payload(LOGIN_URL, BASE_URL, USERNAME, PASSWORD)
    cookie_name = "PPLoggedIn"
    session.login(post_url, payload, cookie_name)
    print(f'is logged in {session._isloggedin}')

    # parse the page to look for all course ids
    base_page_path = session.request_page(BASE_URL)
    base_page = Page(base_page_path)
    links = base_page.get_links()
    idlinks = listf.filter_list(links, "\/launchCourse.do\?id=\d")
    ids = listf.trim_list(idlinks, "([^\d])")

    # use ids to start a new request
    ids = listf.remove_duplicates(ids)
    for id in ids:
        course_page_path = session.request_page(BASE_URL + f'/launchCourse.do?id={id}')
        course_page = Page(course_page_path)
        course_links = course_page.get_links(("div", {"id": "courseMainBox"}))
        filtered_course_links = listf.filter_list(course_links, "\/content.do\?id=\d")
        course_ids = listf.extract_list(filtered_course_links, "id=(\d)*")
        course_ids = listf.remove_duplicates(course_ids)
        course_ids = listf.trim_list(course_ids, "([^\d])")

        for course_id in course_ids:
            content_page_path = session.request_page(BASE_URL + f'/courseId/{id}/content.do?id={course_id}')
            content_page = Page(content_page_path)
            active_text = content_page.text([["a", {"class": "active"}]])
            attr_list = content_page.attributes([["iframe"]], "src")
            ppf_link = attr_list[0]

            ppf_page_path = session.request_page(BASE_URL + ppf_link)
            ppf_page = Page(ppf_page_path)
            text = visualize_page_text(ppf_page)
            listf.print_list(text)

            print("*" * 30)

        print("-" * 20)


def wiki_test():
    new_session = Session(False)
    for _ in range(30):
        path = new_session.request_page("https://en.wikipedia.org/wiki/Special:Random")
        page = Page()
        page.load(path)
        listf.print_list(page.get_links())


def login(session, form_url):
    pass


def facebook_test():
    session = Session(False)
    session.set_headers()
    base_url = "https://m.facebook.com"
    login_url = "https://m.facebook.com/login/?ref=dbl&fl"
    post_url, payload = create_payload(base_url, login_url, FA_USERNAME, FA_PASSWORD)
    session.login(post_url, payload)

    front_page_path = session.request_page("https://m.facebook.com/anton.maxen")
    front_page = Page(front_page_path)
    front_page.trim([["script"]])
    #front_page.remove_comments()
    print(visualize_page_text(front_page))


def main():
    #pingpong_test()
    wiki_test()
    #facebook_test()


if __name__ == '__main__':
    main()
