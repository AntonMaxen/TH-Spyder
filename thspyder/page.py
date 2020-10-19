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
    def __init__(self, file=None):
        self.page = None
        if file is not None:
            self.load(file)

    def load(self, fullpath):
        with open(fullpath, "rb") as p_file:
            unpickled_page = pickle.load(p_file)
            self.page = BeautifulSoup(unpickled_page.text, 'html.parser')

    def get_outer_element(self, identifier=None):
        if identifier is None:
            root = self.page
        else:
            root = self.page.find(*identifier)

        # This can cause unexpected behaviour, need better error management. #TODO
        return root if root is not None else self.page
        # return self.page if identifier is None else self.page.find(*identifier)

    def trim(self, identifiers):
        if self.page is None:
            return False

        if len(identifiers) != 0:
            for identifier in identifiers:
                for element in self.page.find_all(*identifier):
                    element.decompose()

    def remove_comments(self):
        comments = self.page.find_all(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

    def extract(self):
        pass

    def text(self, identifiers, outer_element=None):
        if len(identifiers) == 0:
            return False

        container = self.get_outer_element(outer_element)

        text_elements = []

        for identifier in identifiers:
            for element in container.find_all(*identifier):
                if element.text:
                    text_elements.append(element.text)

        text_elements = [el.text for identifier in identifiers
                         for el in container.find_all(*identifier)
                         if element.text]

        return text_elements

    def attributes(self, identifiers, attrname, outer_element=None):
        if len(identifiers) == 0:
            return False

        container = self.get_outer_element(outer_element)

        attribute_list = []
        for identifier in identifiers:
            for element in container.find_all(*identifier):
                if element.has_attr(attrname):
                    attribute_list.append(element[attrname])

        return attribute_list

    def element(self, identifier, outer_element=None):
        container = self.get_outer_element(outer_element)
        return container.find(*identifier)

    def elements(self, identifier, outer_element=None):
        container = self.get_outer_element(outer_element)
        return container.find_all(*identifier)

    def text_elements(self, outer_element=None):
        container = self.get_outer_element(outer_element)
        return container.find_all(text=True)

    # simple functions
    def get_links(self, outer_element=None):
        return self.attributes([["a"]], "href", outer_element)

    def get_text(self, outer_element=None):
        return self.text([["body"]], outer_element)

    # experimental functions
    def login_fields(self):
        form_variations = {
            'login_names': ['email', 'username', 'user', 'login'],
            'password_names': ['pass', 'password']
        }

        form_element = self.element([["form"]])
        if form_element:
            attr_list = self.attributes([["input", {'type': 'text'}],
                                         ["input", {'type': 'email'}]], "name", "form")

            all_attrs = self.attributes([["input"]], "name", "form")
            all_attrs_value = self.attributes([["input"]], "value", "form")
            data_dict = dict(zip(all_attrs, all_attrs_value))

            un_name = [attr for attr in attr_list if attr in form_variations['login_names']]
            pa_name = self.attributes([["input", {'type': 'password'}]], "name", "form")
            un_name = un_name[0] if len(un_name) > 0 else None
            pa_name = pa_name[0] if len(pa_name) > 0 else None

            # quickfix for enctypes that takes url params as form actions.
            if 'enctype' in form_element:
                if form_element['enctype'] != "application/x-www-form-urlencoded":
                    action = form_element['action']
                else:
                    action = ''
            else:
                action = form_element['action']

            return {
                'action': action,
                'un_name': un_name,
                'pa_name': pa_name,
                'data': data_dict
            }


def main():
    pass


if __name__ == '__main__':
    main()
