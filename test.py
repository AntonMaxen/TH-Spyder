import requests
from bs4 import BeautifulSoup
from thspyder.page import Page
from thspyder.helpers.listf import print_list
from urllib.parse import urlparse
import os.path


def main():
    url = "https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=uvlaiki"
    session = requests.session()
    req = session.get(url, headers=dict(referer=url))
    page = BeautifulSoup(req.content, 'html.parser')
    my_page = Page(page=page)
    print_list(my_page.get_text(["div", {"id": "contentHiscores"}]))

    for _ in None:
        print("hello")

    pass

def url_test():
    url = "https://www.m.example.com/home"
    parsed_url = urlparse(url)
    if None:
        print("hello")

    print(__file__)



    pass


if __name__ == '__main__':
    url_test()
