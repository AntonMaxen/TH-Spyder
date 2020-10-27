import os
from dotenv import load_dotenv

from thspyder.bot import Bot
from thspyder.models import model_rs as something_fun

load_dotenv()
WHOOK = os.getenv("WHOOK")

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

def main():
    bot = Bot()
    bot.add_spider(model_rs, WHOOK, day_of_week="*", hour="0-23", minute="0/5")
    bot.load_spiders()
    bot.start()


if __name__ == '__main__':
    main()
