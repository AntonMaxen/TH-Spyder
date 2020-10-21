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
        "file_name": "youtube_links",
        "elements": [["iframe"]],
        "attributes": ['src'],
        "root": None
    },
    {
        "file_name": "image_links",
        "elements": [["img"]],
        "attributes": ['src'],
        "root": None
    },
    {
        "file_name": "links",
        "elements": [[True]],
        "attributes": ['src', 'href'],
        "root": None
    }
]

WANTED_TEXT = [
    {
        "file_name": "site_text",
        "elements": [["p"], ["h3"]],
        "root": None
    },
    {
        "file_name": "table_text",
        "elements": [['tr']],
        "root": ["div", {"id": "contentHiscores"}]
    }
]

UNWANTED_ELEMENTS = [
    ["script"],
    ["head"]
]

modelpp = {
    "name": "pingpong",
    "login": {
        "form_url": LOGIN_URL,
        "auth_cookie": AUTH_COOKIE,
        "username": USERNAME,
        "password": PASSWORD
    },
    "scrape_url": SCRAPE_URL,
    "wanted_attributes": WANTED_ATTRIBUTES,
    "wanted_text": WANTED_TEXT,
    "unwanted_elements": []
}

model_wiki = {
    "name": "wikipedia",
    "scrape_url": "https://en.wikipedia.org/wiki/George_Black_(New_Zealand_politician)",
    "wanted_attributes": WANTED_ATTRIBUTES,
    "wanted_text": WANTED_TEXT,
    "unwanted_elements": UNWANTED_ELEMENTS

}


model_wiki_random = {
    "name": "wikipedia",
    "scrape_url": "https://en.wikipedia.org/wiki/Special:Random",
    "wanted_attributes": WANTED_ATTRIBUTES,
    "wanted_text": WANTED_TEXT,
    "unwanted_elements": UNWANTED_ELEMENTS

}

model_rs = {
    "name": "runescape",
    "scrape_url": "https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=uvlaiki",
    "wanted_attributes": WANTED_ATTRIBUTES,
    "wanted_text": WANTED_TEXT,
    "unwanted_elements": UNWANTED_ELEMENTS,
}


def main():
    pass


if __name__ == '__main__':
    main()
