model_rs = {
    "name": "runescapeHiscores",
    "scrape_url": "https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=uvlaiki",
    "wanted_attributes": [],
    "wanted_text": [
        {
            "file_name": "table.txt",
            "elements": "tr",
            "root": ["div", {"id": "contentHiscores"}],
            "strip": True,
            "separator": "|"

        }
    ],
    "unwanted_elements": [],
}