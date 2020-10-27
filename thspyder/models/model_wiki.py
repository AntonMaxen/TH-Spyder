from thspyder.models.default import WANTED_TEXT, WANTED_ATTRIBUTES, UNWANTED_ELEMENTS
model_wiki = {
    "name": "wikipedia",
    "scrape_url": "https://en.wikipedia.org/wiki/George_Black_(New_Zealand_politician)",
    "wanted_attributes": WANTED_ATTRIBUTES,
    "wanted_text": WANTED_TEXT,
    "unwanted_elements": UNWANTED_ELEMENTS

}

model_wiki_random = {
    "name": "wikipedia",
    "scrape_url": "https://en.wikipedia.org/wiki/Special:Random",
    "wanted_attributes": WANTED_ATTRIBUTES,
    "wanted_text": WANTED_TEXT,
    "unwanted_elements": UNWANTED_ELEMENTS

}
