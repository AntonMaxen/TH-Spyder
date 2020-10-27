import os
from dotenv import load_dotenv
load_dotenv()


USERNAME = os.getenv('PP_USERNAME')
PASSWORD = os.getenv('PP_PASSWORD')
LOGIN_URL = "https://yh.pingpong.se/login/processlogin?disco=local"
SCRAPE_URL = "https://yh.pingpong.se/pp/courses/course11264/published/1603131345825/resourceId/4980914/content/5e4540d8-7a81-4bb2-afc7-c4de59000348/5e4540d8-7a81-4bb2-afc7-c4de59000348.html"
AUTH_COOKIE = "PPLoggedIn"


WANTED_ATTRIBUTES = [
    {
        "file_name": "youtube_links.txt",
        "elements": "iframe",
        "attributes": "src",
        "replace": ("//www.youtube.com/embed", "https://youtu.be"),
        "sub": ("(\\?ecver=\\d)", ""),
        "root": None
    },
    {
        "file_name": "image_links.txt",
        "elements": "img",
        "attributes": "src",
        "root": None
    },
    {
        "file_name": "links.txt",
        "elements": [[True]],
        "attributes": ["src", "href"],
        "root": None
    }
]

WANTED_TEXT = [
    {
        "file_name": "site_text.txt",
        "elements": ["p", "h3"],
        "root": None,
        "strip": False,
        "separator": ""
    },
    {
        "file_name": "all-text.txt",
        "elements": "body",
        "root": None,
        "strip": True,
        "separator": "\n"

    },
    {
        "file_name": "table_text.txt",
        "elements": "tr",
        "root": ["div", {"id": "contentHiscores"}],
        "strip": True,
        "separator": "|"
    }
]

UNWANTED_ELEMENTS = [
    "script",
    "head"
]


def auth_function(session):
    return len([cookie for cookie in session.cookies if cookie.name == AUTH_COOKIE]) > 0


modelpp = {
    "name": "pingpong",
    "login": {
        "form_url": LOGIN_URL,
        "auth_func": auth_function,
        "username": USERNAME,
        "password": PASSWORD
    },
    "scrape_url": SCRAPE_URL,
    "wanted_attributes": WANTED_ATTRIBUTES,
    "wanted_text": WANTED_TEXT,
    "unwanted_elements": []
}


class Model:
    def __init__(self, name="", login=None, scrape_url="",
                 wanted_attributes=None, wanted_text=None,
                 unwanted_elements=None):

        self.name = name or "default"
        self.login = login
        self.scrape_url = login or "https://example.com"
        self.wanted_attributes = build_attributes(wanted_attributes)
        self.wanted_text = []
        self.unwanted_elements = []
        pass


def build_attributes(wanted_attr):
    if wanted_attr is None or len(wanted_attr) == 0:
        return []
    """
    
    for attr_dict in wanted_attr:
        if
    """

def fill_if_not_exist(my_dict):
    pass

def main():
    pass


if __name__ == '__main__':
    main()
