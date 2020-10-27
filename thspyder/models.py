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
        "elements": [["iframe"]],
        "attributes": ['src'],
        "root": None
    },
    {
        "file_name": "cool_links.txt",
        "elements": [["img"]],
        "attributes": ['src'],
        "root": None

    },
    {
        "file_name": "links.txt",
        "elements": [[True]],
        "attributes": ['src', 'href'],
        "replace": ("https://www.youtube.com/embed", "https://youtu.be"),
        "sub": ("(\\?ecver=\\d)", ""),
        "root": None
    }
]


WANTED_TEXT = [
    {
        "file_name": "site_text.txt",
        "elements": [["p"], ["h3"]],
        "root": None,
        "strip": False,
        "separator": ""
    },
    {
        "file_name": "all-text.txt",
        "elements": [["body"]],
        "root": None,
        "strip": True,
        "separator": "\n"

    },
    {
        "file_name": "table_text.txt",
        "elements": [['tr']],
        "root": ["div", {"id": "contentHiscores"}],
        "strip": True,
        "separator": "|"
    }
]

UNWANTED_ELEMENTS = [
    ["script"],
    ["head"]
]

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


default_model = {
    "name": "example",
    "scrape_url": "https://example.com/",
    "wanted_attributes": [],
    "wanted_text": [
        {
            "file_name": "site_text.txt",
            "elements": [["body"]],
            "root": None,
            "strip": False,
            "separator": ""
        }
    ],
    "unwanted_elements": []
}


def main():
    pass


if __name__ == '__main__':
    main()
