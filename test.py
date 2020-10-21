import requests
from bs4 import BeautifulSoup
from thspyder.page import Page
from thspyder.helpers.listf import print_list

def main():
    url = "https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=uvlaiki"
    session = requests.session()
    req = session.get(url, headers=dict(referer=url))
    page = BeautifulSoup(req.content, 'html.parser')
    my_page = Page(page=page)
    print_list(my_page.get_text(["div", {"id": "contentHiscores"}]))

    pass


if __name__ == '__main__':
    main()
