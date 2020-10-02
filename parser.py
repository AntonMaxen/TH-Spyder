import pickle
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


class Parser:
    def __init__(self):
        self.page = None

    def load(self, filename):
        with open(filename, "rb") as p_file:
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

    def extract(self):
        pass


def main():
    myParser = Parser()
    myParser.load("yh.pingpong.se.pickle")
    #print(myParser.page)
    unwanted_elements = [
        ["head"],
        ["div", {"id": "header"}],
        ["script"],
        ["header"]
    ]
    myParser.trim(unwanted_elements)
    print("-" * 20)
    print(myParser.page.prettify())


def test():
    myJunk = BeautifulSoup('<div class="canvas-body">Hello i like me some sugar</div>', 'html.parser')
    result = myJunk.find_all('div "class": "canvas-body"')
    myList = ["div", {"class": "canvas-body"}]


if __name__ == '__main__':
    main()
    #test()
