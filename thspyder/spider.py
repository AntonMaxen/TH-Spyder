import os
import shutil
import time

# local imports
from thspyder.session import Session
from thspyder.page import Page
from thspyder.helpers.utils import create_payload
from thspyder.helpers.writefile import update_file
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

    def run(self):
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
            self.save_result(timestamp, constants.ATTRIBUTE_FOLDER, attribute['file_name'], attributes)

        # extracts wanted text
        for el in self.wanted_text:
            found_text = content_page.text(el['elements'], el['root'], strip=el['strip'], sep=el['separator'])

            self.save_result(timestamp, constants.TEXT_FOLDER, el['file_name'], found_text)

    def login(self):
        post_url, payload = create_payload(self.form_url, self.username, self.password)
        self.session.login(post_url, payload, self.auth_func)
        if not self.session.isloggedin:
            raise Exception("login failed")

    def save_result(self, timestamp, folder_name, file_name, result_list):
        path = (self.spider_name, timestamp, folder_name)
        for result in result_list:
            updated = update_file(result, path, file_name)
            if updated:
                #print(f"the page: {'/'.join(path)}/{file_name} is updated with: {str(len(result))} lines")
                pass
            else:
                #print("|-|"*30)
                pass


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
        default_spider.run()
        spyder.run()
        wiki_spider.run()
        rs_spider.run()


if __name__ == '__main__':
    main()
