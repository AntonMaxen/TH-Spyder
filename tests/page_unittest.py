from thspyder.page import Page
import unittest
from bs4 import Comment

CONTENT_PATH = "material/pages/content.pickle"
FORM_PATH = "material/pages/form.pickle"


class TestPage(unittest.TestCase):
    page = Page()

    def test_Page_load(self):
        self.page.load(CONTENT_PATH)
        self.assertEqual(self.page.page.title.text, "Python (programming language) - Wikipedia")

    def test_Page_get_outer_element(self):
        self.page.load(CONTENT_PATH)
        self.assertEqual(self.page.get_outer_element("body").name, "body")
        self.assertEqual(self.page.get_outer_element(["body"]).name, "body")
        self.assertEqual(self.page.get_outer_element(("body",)).name, "body")
        self.assertEqual(self.page.get_outer_element(["body", {"class": "mediawiki"}]).name, "body")

    def test_Page_trim(self):
        self.page.load(CONTENT_PATH)
        self.page.trim("body")
        self.assertEqual(self.page.get_outer_element("body").name, "[document]")

    def test_Page_remove_comments(self):
        self.page.load(CONTENT_PATH)
        self.page.remove_comments()
        self.assertIsNone(self.page.page.find(text=lambda text: isinstance(text, Comment)))

    def test_Page_elements(self):
        self.page.load(CONTENT_PATH)

        def inner_function(el):
            if el.has_attr("id"):
                return el['id']

        self.assertListEqual(self.page.elements("a", inner_function), ['top'])

    def test_Page_attributes(self):
        self.page.load(CONTENT_PATH)
        self.assertEqual(len(self.page.attributes([["div", {"class": "noprint"}]], "class")), 5)
        self.assertEqual(len(self.page.attributes("div", "class")), 62)

    def test_Page_text(self):
        self.page.load(CONTENT_PATH)
        self.assertEqual(len(self.page.text("p", strip=True)), 80)
        self.assertEqual(len(self.page.text("td", outer_element=("table", {"class": "wikitable"}), strip=True)), 64)

    def test_Page_find_element(self):
        self.page.load(CONTENT_PATH)
        self.assertEqual(self.page.find_element("form")['action'], "/w/index.php")

    def test_Page_find_elements(self):
        self.page.load(CONTENT_PATH)
        self.assertEqual(len(self.page.find_elements(["span", {"class": True}])), 1215)

    def test_Page_get_links(self):
        self.page.load(CONTENT_PATH)
        self.assertEqual(len(self.page.get_links()), 1736)

    def test_Page_login_fields(self):
        self.page.load(FORM_PATH)
        login_fields = self.page.login_fields()
        form_attrs = login_fields['form_attrs']
        input_names = login_fields['input_names']
        self.assertDictEqual(form_attrs, {
            'method': 'post',
            'enctype': 'application/x-www-form-urlencoded',
            'autocomplete': 'off',
            'accept-charset': ['UTF-8'],
            'action': '/login/processlogin',
            'class': ['login__type']
        })
        self.assertEqual(login_fields['login_name'], "login")
        self.assertEqual(login_fields['password_name'], "password")
        self.assertDictEqual(input_names, {
            'handleJavascriptCheck': 'true',
            'javascriptEnabled': 'false',
            'screenWidth': '',
            'screenHeight': '',
            'disco': 'local',
            'targeturl': '/startPage.do',
            'login': '',
            'password': ''
        })


if __name__ == '__main__':
    unittest.main()
