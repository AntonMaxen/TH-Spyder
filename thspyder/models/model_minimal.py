minimal_model = {
    "name": "minimal",
    "scrape_url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "wanted_text": [
        {
            "file_name": "minimal.txt",
            "elements": "h1"
        },
        {
            "file_name": "all_text.txt",
            "elements": "body",
            "separator": "\n",
            "strip": True
        },
        {
            "file_name": "table_text.txt",
            "elements": "tr",
            "strip": True,
            "separator": " ",
            "root": "table"

        }
    ],
    "wanted_attributes": [
        {
            "file_name": "all_links.txt",
            "elements": [[True]],
            "attributes": ["src", "href"]
        }
    ]
}
