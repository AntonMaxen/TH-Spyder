import os
import shutil
import time
import re

# local imports
from thspyder.session import Session
from thspyder.page import Page
from thspyder.fileprocessor import FileProcessor
from thspyder.helpers.utils import create_payload
from thspyder.helpers.writefile import write_file
from thspyder.helpers.listf import remove_junk, print_list, trim_list, strip_list, unidecode_list
from thspyder.models import model_rs, model_wiki, default_model
from thspyder.model_pp import modelpp
import thspyder.helpers.myconstants as constants


class Spider:
    def __init__(self, model):
        self.spider_name = model['name']
        if 'login' in model:
            self.login_required = True
            self.form_url = model['login']['form_url']
            self.auth_func = model['login']['auth_func']
            self.username = model['login']['username']
            self.password = model['login']['password']
        else:
            self.login_required = False

        self.scrape_url = model['scrape_url']
        self.wanted_attributes = model['wanted_attributes']
        self.wanted_text = model['wanted_text']
        self.unwanted_elements = model['unwanted_elements']
        self.session = None
        self.file_processor = FileProcessor((constants.STORAGE_FOLDER, constants.DATA_FOLDER), self.spider_name)

    def scrape(self):
        # does one iteration of scraping

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
        for attribute in self.wanted_attributes:
            attributes = content_page.attributes(attribute['elements'], attribute['attributes'], attribute['root'])
            attributes = reformat_list_items(attribute, attributes)
            self.save_result(timestamp, constants.ATTRIBUTE_FOLDER, attribute['file_name'], attributes)

        # extracts wanted text
        for el in self.wanted_text:
            found_text = content_page.text(el['elements'], el['root'], strip=el['strip'], sep=el['separator'])
            found_text = reformat_list_items(el, found_text)
            self.save_result(timestamp, constants.TEXT_FOLDER, el['file_name'], found_text)

    def login(self):
        post_url, payload = create_payload(self.form_url, self.username, self.password)
        self.session.login(post_url, payload, self.auth_func)
        if not self.session.isloggedin:
            raise Exception("login failed")

    def save_result(self, timestamp, folder_name, file_name, result_list):
        path = (self.spider_name, timestamp, folder_name)
        write_file(result_list, path, file_name)

    def get_difference_recent(self):
        return self.file_processor.file_diff_recent()

    def scrape_and_get_difference(self):
        self.scrape()
        return self.get_difference_recent()


def reformat_list_items(config, my_list):
    reformatted_list = my_list.copy()
    if "replace" in config:
        reformatted_list = [item.replace(*config['replace']) for item in reformatted_list]

    if "sub" in config:
        reformatted_list = [re.sub(*config['sub'], item) for item in reformatted_list]

    return reformatted_list


def remove_data():
    if os.path.exists("data"):
        shutil.rmtree("data")


def main():
    default_spider = Spider(default_model)
    rs_spider = Spider(model_rs)
    spyder = Spider(modelpp)
    wiki_spider = Spider(model_wiki)
    times = 1

    for _ in range(times):
        print(default_spider.scrape_and_get_difference())
        print(spyder.scrape_and_get_difference())
        print(wiki_spider.scrape_and_get_difference())
        print(rs_spider.scrape_and_get_difference())


if __name__ == '__main__':
    main()
