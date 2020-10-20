from urllib.parse import urlparse
# local imports
from thspyder.session import Session
from thspyder.page import Page
from thspyder.helpers.listf import print_list, remove_junk


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


def main():
    pass


if __name__ == '__main__':
    main()
