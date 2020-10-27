WANTED_ATTRIBUTES = [
    {
        "file_name": "youtube_links.txt",
        "elements": "iframe",
        "attributes": "src",
        "replace": ("//www.youtube.com/embed", "https://youtu.be"),
        "sub": ("(\\?ecver=\\d)", ""),
        "root": None
    },
    {
        "file_name": "cool_links.txt",
        "elements": "img",
        "attributes": "src",
        "root": None

    },
    {
        "file_name": "links.txt",
        "elements": [[True]],
        "attributes": ['src', 'href'],
        "root": None
    }
]


WANTED_TEXT = [
    {
        "file_name": "site_text.txt",
        "elements": ["p", "h3"],
        "root": None,
        "strip": False,
        "separator": ""
    },
    {
        "file_name": "all-text.txt",
        "elements": "body",
        "root": None,
        "strip": True,
        "separator": "\n"

    },
    {
        "file_name": "table_text.txt",
        "elements": "tr",
        "root": ["div", {"id": "contentHiscores"}],
        "strip": True,
        "separator": "|"
    }
]

UNWANTED_ELEMENTS = ["head", "script"]

default_model = {
    "name": "example",
    "scrape_url": "https://example.com/",
    "wanted_attributes": WANTED_ATTRIBUTES,
    "wanted_text": WANTED_TEXT,
    "unwanted_elements": UNWANTED_ELEMENTS
}
