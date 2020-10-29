import time
import re

# local imports
from thspyder.session import Session
from thspyder.page import Page
from thspyder.fileprocessor import FileProcessor
from thspyder.helpers.utils import create_payload
from thspyder.helpers.writefile import write_file
import thspyder.helpers.myconstants as constants


class Spider:
    """Class Spider is a scraping class that with a given model,
    can make a round of scraping"""
    def __init__(self, model):
        self.session = None
        self.spider_name = model['name']
        if 'login' in model:
            self.login_required = True
            self.form_url = model['login']['form_url']
            self.auth_func = model['login'].get('auth_func', None)
            self.username = model['login']['username']
            self.password = model['login']['password']
        else:
            self.login_required = False

        self.scrape_url = model['scrape_url']
        self.wanted_attributes = model.get("wanted_attributes", [])
        self.wanted_text = model.get("wanted_text", [])
        self.unwanted_elements = model.get("unwanted_elements", [])
        self.file_processor = FileProcessor((constants.STORAGE_FOLDER, constants.DATA_FOLDER), self.spider_name)

    def scrape(self):
        """does one iteration of scraping"""

        # one timestamp for whole run.
        timestamp = str(round(time.time()))
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
        for at in self.wanted_attributes:
            file_name = at['file_name']
            elements = at['elements']
            attributes = at['attributes']
            root = at.get("root", None)
            found_attributes = content_page.attributes(elements, attributes, outer_element=root)
            found_attributes = reformat_list_items(at, found_attributes)
            self.save_result(timestamp, constants.ATTRIBUTE_FOLDER, file_name, found_attributes)

        # extracts wanted text
        for el in self.wanted_text:
            file_name = el['file_name']
            elements = el['elements']
            root = el.get("root", None)
            strip = el.get("strip", False)
            sep = el.get("separator", "")
            found_text = content_page.text(elements, outer_element=root, strip=strip, sep=sep)
            found_text = reformat_list_items(el, found_text)
            self.save_result(timestamp, constants.TEXT_FOLDER, file_name, found_text)

    def login(self):
        """builds a payload from attributes and issues a login request with session"""
        post_url, payload = create_payload(self.form_url, self.username, self.password)
        self.session.login(post_url, payload, auth_func=self.auth_func)
        if not self.session.isloggedin:
            raise Exception("login failed")

    def save_result(self, timestamp, folder_name, file_name, result_list):
        """writes a given list to a file with given path to that file"""
        path = (self.spider_name, timestamp, folder_name)
        write_file(result_list, path, file_name)

    def get_difference_recent(self):
        """returns dict of difference between 2 recent scrapes"""
        return self.file_processor.file_diff_recent()

    def scrape_and_get_difference(self):
        """scrapes and returns dict of difference between 2 recent scrapes"""
        self.scrape()
        return self.get_difference_recent()


def reformat_list_items(config, my_list):
    """reformats list according to a config"""
    reformatted_list = my_list.copy()
    if "replace" in config:
        reformatted_list = [item.replace(*config['replace']) for item in reformatted_list]

    if "sub" in config:
        reformatted_list = [re.sub(*config['sub'], item) for item in reformatted_list]

    return reformatted_list
