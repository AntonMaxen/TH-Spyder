import pickle
from bs4 import BeautifulSoup
from bs4 import Comment

"""
    Identifier model:
    ["element", {attribute dict}]
    
    example:
    ["h3", {"class": "fancy"}]
    unpacks into
    h3, {"class": "fancy"}
    
    bs4 find method takes
    name, attrdict
    
    unwanted_elements = [["h3"], ["meta", {"charset": "utf-8"}], ["div", {"class": "box without-header"}]]
"""


class Page:
    """class Page is a Parser containing methods for easier data extraction from htmltrees"""
    def __init__(self, file=None, page=None):
        self.page = page
        if file is not None:
            self.load(file)

    def load(self, fullpath):
        """loads a pickled htmltree from a pickle file using filepath"""
        with open(fullpath, "rb") as p_file:
            unpickled_page = pickle.load(p_file)
            self.page = BeautifulSoup(unpickled_page.text, 'html.parser')

    def get_outer_element(self, identifier=None):
        """returns element matching given html identifier, if not found returns page"""
        if self.page is None:
            raise Exception("missing classmember Page.page")

        if identifier is None:
            return self.page

        identifier = str_to_list(identifier)
        root = self.page.find(*identifier)

        return root if root is not None else self.page

    def trim(self, identifiers):
        """removes matching elementes according to identifier from page attribute"""
        if self.page is None:
            raise Exception("missing classmember Page.page")

        identifiers = str_to_list(identifiers)
        for identifier in identifiers:
            identifier = str_to_list(identifier)

            for element in self.page.find_all(*identifier):
                element.decompose()

    def remove_comments(self):
        """removes html comments from htmltree"""
        if self.page is None:
            raise Exception("missing classmember Page.page")

        comments = self.page.find_all(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

    def elements(self, identifiers, func, outer_element=None):
        """locates all elements matching identifier and return all items according to
        a given function."""
        container = self.get_outer_element(outer_element)

        items = []

        identifiers = str_to_list(identifiers)
        for identifier in identifiers:
            identifier = str_to_list(identifier)

            for element in container.find_all(*identifier):
                item = func(element)
                if item:
                    items.append(item)

        return items

    def text(self, identifiers, outer_element=None, sep="", strip=False):
        """locates all elements matching identifier and returns all those elements
        who have text"""
        def extract(element):
            if element.text:
                return element.get_text(separator=sep, strip=strip)

        return self.elements(identifiers, extract, outer_element)

    def attributes(self, identifiers, attrnames, outer_element=None):
        """locates all elements matching identifier and returns attribute value of element
        if element got that given attribute"""
        def extract(element):
            l_attrnames = str_to_list(attrnames)
            for attrname in l_attrnames:
                if element.has_attr(attrname):
                    return element[attrname]

        return self.elements(identifiers, extract, outer_element)

    # development methods
    def find_element(self, identifier, outer_element=None):
        """returns bs4 element matching identifier"""
        container = self.get_outer_element(outer_element)
        identifier = str_to_list(identifier)
        return container.find(*identifier)

    def find_elements(self, identifier, outer_element=None):
        """returns bs4 elements matching identifier"""
        container = self.get_outer_element(outer_element)
        identifier = str_to_list(identifier)
        return container.find_all(*identifier)

    # simple functions
    def get_links(self, outer_element=None):
        """returns all links on page"""
        return self.attributes("a", "href", outer_element)

    def get_text(self, outer_element=None):
        """return all text on page"""
        container = self.get_outer_element(outer_element)
        return container.stripped_strings

    # experimental functions
    def login_fields(self):
        """returns structured dict of the form in page"""
        login_variations = ['email', 'username', 'user', 'login']

        form_element = self.find_element("form")
        if form_element:
            attr_list = self.attributes([["input", {'type': 'text'}],
                                         ["input", {'type': 'email'}]], "name", "form")

            input_elements = self.find_elements(["input", {"name": True}], "form")
            input_dict = {}
            for element in input_elements:
                if element.has_attr('value'):
                    input_dict[element['name']] = element['value']
                else:
                    input_dict[element['name']] = ""

            login_name = [attr for attr in attr_list if attr in login_variations]
            password_name = self.attributes([["input", {'type': 'password'}]], "name", "form")
            login_name = login_name[0] if len(login_name) > 0 else None
            password_name = password_name[0] if len(password_name) > 0 else None

            return {
                'form_attrs': form_element.attrs,
                'login_name': login_name,
                'password_name': password_name,
                'input_names': input_dict
            }


def str_to_list(string):
    return [string] if isinstance(string, str) else string

