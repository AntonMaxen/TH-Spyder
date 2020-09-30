import requests
import pickle
import random
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import helper

load_dotenv()


class Model:
    def __init__(self, base_url, source_url, login_url, root_element, unwanted_elements, hooks):
        self._model = {
            'base_url': base_url,
            'source_url': source_url,
            'login_url': login_url,
            'root_element': root_element,
            'unwanted_elements': unwanted_elements,
            'hooks': hooks
        }

    def __str__(self):
        return f"""
            'base_url': {self._model['base_url']}
            'source_url': {self._model['source_url']}
            'login_url' : {self._model['login_url']}
            'root_element': {self._model['root_element']}
            'unwanted_elements': {self._model['unwanted_elements']}
            'hooks': {self._model['hooks']}
        """


class Session:
    def __init__(self, model):
        self._session = requests.session()
        self.model = model._model
        pass

    def login(self):
        pass



class Spider:
    def __init__(self, model):
        self.model = model._model
        self.filename = None
        self.session = Session(self.model)

    def login(self):
        # set payload
        # create session
        # build header
        # post request with login url
        # validate login success
        # return session
        return object

    def request_page(self):
        # build header
        # get url w or w/o session
        # pickle the page
        return "filedestination"

    def validate_page(self):
        # unpickle page
        # read status code
        # if !ok queue another request
        # else queue for processing/parsing
        pass

    def process_page(self):
        # get unpickled page
        # get root(container) element with bs4
        # trim junk from container
        # Process remaining and extract wanted information
        pass


if __name__ == '__main__':
    myModel = Model(
        "https://yh.pingpong.se",
        "https://yh.pingpong.se/courseId/11264/content.do?id=4744630",
        "https://yh.pingpong.se/login/processlogin?disco=local",
        {'div': 'class="main"'},
        ["p", "li", "ul"],
        [{'div': 'id="super_secret_id"'}]
    )

    print(myModel)

    mySpider = Spider(myModel)
    print(mySpider.filename)

    session = mySpider.login()
    filename = mySpider.request_page()
    if mySpider.validate_page():
        mySpider.process_page()
