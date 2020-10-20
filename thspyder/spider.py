import os
from dotenv import load_dotenv

# local imports
from thspyder.session import Session
from thspyder.page import Page
from thspyder.helpers.utils import create_payload
from thspyder.helpers.writefile import update_file
from thspyder.helpers.listf import remove_junk
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
        "attribute": "src"
    },
    {
        "file_name": "image_links",
        "elements": [["img"]],
        "attribute": "src"
    },
    {
        "file_name": "links",
        "elements": [[True]],
        "attribute": "src"
    },
    {
        "file_name": "links",
        "elements": [[True]],
        "attribute": "href"
    }
]

WANTED_TEXT = [
    {
        "file_name": "site_text",
        "elements": [["p"], ["h3"]]
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


class Spider:
    def __init__(self, model):
        self.spider_name = model['name']
        if 'login' in model:
            self.login_required = True
            self.form_url = model['login']['form_url']
            self.auth_cookie = model['login']['auth_cookie']
            self.username = model['login']['username']
            self.password = model['login']['password']
        else:
            self.login_required = False

        self.scrape_url = model['scrape_url']
        self.wanted_attributes = model['wanted_attributes']
        self.wanted_text = model['wanted_text']
        self.unwanted_elements = model['unwanted_elements']
        self.session = None

    def run(self):
        # does one iteration of scraping

        self.session = Session(self.login_required)
        # login if required
        if self.login_required:
            self.login()

        # downloads page and creates a Page object for parsign
        content_page_path = self.session.request_page(self.scrape_url)
        content_page = Page(content_page_path)

        # trim unwanted elements from page object
        content_page.trim(self.unwanted_elements)

        # extracts wanted attributes
        for attribute in self.wanted_attributes:
            found_attributes = content_page.attributes(attribute['elements'], attribute['attribute'])
            self.save_result("attribute", attribute['file_name'], found_attributes)

        # extracts wanted text
        for element in self.wanted_text:
            # found_text = content_page.text(element['elements'])
            # found_text = content_page.get_text()
            found_text = content_page.text_elements()
            found_text = remove_junk(found_text)
            self.save_result("text", element['file_name'], found_text)

    def login(self):
        post_url, payload = create_payload(self.form_url, self.username, self.password)
        self.session.login(post_url, payload, self.auth_cookie)
        if not self.session.isloggedin:
            raise Exception("login failed")

    def save_result(self, category, file_name, result_list):
        for result in result_list:
            updated = update_file(result, f'{self.spider_name}/{category}', f'{file_name}.txt')
            if updated:
                print("the page is updated with" + str(result))


if __name__ == '__main__':
    spyder = Spider(modelpp)
    spyder.run()

    wiki_spider = Spider(model_wiki)
    wiki_spider.run()
    pass
