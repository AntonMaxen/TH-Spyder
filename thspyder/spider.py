import os

# local imports
from thspyder.session import Session
from thspyder.page import Page
from thspyder.helpers.utils import create_payload
from thspyder.helpers.writefile import update_file
from thspyder.helpers.listf import remove_junk, print_list, trim_list, strip_list, unidecode_list
from thspyder.models import model_rs, modelpp, model_wiki


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
            attributes = content_page.attributes(attribute['elements'], attribute['attributes'], attribute['root'])
            self.save_result("attributes", attribute['file_name'], attributes)

        # extracts wanted text
        for element in self.wanted_text:
            found_text = content_page.text(element['elements'], element['root'], strip=True, sep="|")
            #found_text = trim_list(found_text, '(\\n)+', " ")
            #found_text = strip_list(found_text)
            print(found_text)

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
                #print("the page is updated with: " + str(result))
                pass


if __name__ == '__main__':
    spyder = Spider(modelpp)
    spyder.run()

    wiki_spider = Spider(model_wiki)
    wiki_spider.run()

    rs_spider = Spider(model_rs)
    rs_spider.run()
    pass
