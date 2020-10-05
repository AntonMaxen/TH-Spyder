import pickle
import re
from bs4 import BeautifulSoup

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


# probably renaming class to page instead of parser, example page.trim, page.extract
class Page:
    def __init__(self):
        self.page = None

    def load(self, fullpath):

        with open(fullpath, "rb") as p_file:
            unpickled_page = pickle.load(p_file)
            self.page = BeautifulSoup(unpickled_page.text, 'html.parser')

    def trim(self, identifiers):
        if self.page is None:
            return False

        if len(identifiers) != 0:
            for identifier in identifiers:
                print(f'identifier {identifier}')
                for element in self.page.find_all(*identifier):
                    print(f'element {type(element)}')
                    element.decompose()

    def outer_element(self, identifier):
        root = self.page.find(*identifier)
        # error handling if root is not found TODO
        return root

    def text(self, identifiers):
        if len(identifiers) == 0:
            return False

        text_elements = []

        for identifier in identifiers:
            for element in self.page.find_all(*identifier):
                if element.text:
                    text_elements.append(element.text)

        return text_elements

    def attributes(self, identifiers, attrname):
        if len(identifiers) == 0:
            return False

        attribute_list = []

        for identifier in identifiers:
            for element in self.page.find_all(*identifier):
                if element.has_attr(attrname):
                    attribute_list.append(element[attrname])

        return attribute_list

    def extract(self):
        pass


def add_prefix(str_list, prefix):
    return [prefix + s for s in str_list]


def reformat_youtube_embed(links):
    new_links = [link.replace('https://www.youtube.com/embed', 'https://youtu.be') for link in links]
    reformatted_links = [re.sub('(\\?ecver=\\d)', '', link) for link in new_links]
    return reformatted_links


def main():
    myPage = Page()
    myPage.load("yh.pingpong.se.pickle")
    #print(myPage.page)
    unwanted_elements = [
        ["head"],
        ["div", {"id": "header"}],
        ["script"],
        ["header"],
        ["h3"]
    ]

    wanted_elements = [
        [True]
    ]

    attr_list = myPage.attributes(wanted_elements, 'src')
    fixed_links = add_prefix(attr_list, 'https:')
    reformatted_links = reformat_youtube_embed(fixed_links)
    for f in reformatted_links:
        print(f)

    #for f in found_text:
        #print(f)

    #myPage.trim(unwanted_elements)
    print("-" * 20)
    #print(myPage.page.prettify())


def test():
    myJunk = BeautifulSoup('<div class="canvas-body">Hello i like me some sugar</div>', 'html.parser')
    result = myJunk.find_all('div "class": "canvas-body"')
    myList = ["div", {"class": "canvas-body"}]


if __name__ == '__main__':
    main()
    #test()
