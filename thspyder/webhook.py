import requests
import json
import time
import os
from dotenv import load_dotenv
load_dotenv()
WHOOK = os.getenv("WHOOK")
MAX_UNICODE_CHARS = 2000


class Webhook:
    def __init__(self, url):
        self.url = url

    def send(self, content, name, ignore_empty=False, formatting="", items_per_request=0, delay=2):
        if ignore_empty:
            content = [line for line in content if line]

        # add formatting
        content = [f'{formatting}{line}{formatting}' if line else line for line in content]
        # split lists for separate requests
        list_of_lists = split_list_in_lists(content, items_per_request)
        splitted_content = [split_list(content, MAX_UNICODE_CHARS) for content in list_of_lists]

        for list_content in splitted_content:
            for c in list_content:
                data = {
                    "content": "\n".join(c),
                    "username": name
                }

                result = requests.post(self.url, data=json.dumps(data), headers={"Content-Type": "application/json"})

                try:
                    result.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    print(err)
                else:
                    print("success")

                if len(list_content) > 1 or len(splitted_content) > 1:
                    time.sleep(delay)


def split_list(my_list, max_chars):
    total = -1
    splitted_lists = []
    temp_list = []
    for string in my_list:
        if total + len(string) + 1 > max_chars:
            total = -1
            splitted_lists.append(temp_list.copy())
            temp_list = [string]
        else:
            temp_list.append(string)

        total += len(string) + 1

    if len(temp_list) > 0:
        splitted_lists.append(temp_list)

    return splitted_lists


def split_list_in_lists(my_list, items_per_request):
    if items_per_request <= 0:
        return [my_list]

    new_list = []
    temp_list = []
    for counter, item in enumerate(my_list):
        temp_list.append(item)
        if (counter + 1) % items_per_request == 0:
            new_list.append(temp_list.copy())
            temp_list = []

    if len(temp_list) > 0:
        new_list.append(temp_list)

    return new_list


def count_chars(my_list):
    total = 0
    for string in my_list:
        total += len(string)
    return total


def main():
    test_list = ['https://www.runescape.com/img/rsp777/hiscores/skill_icon_attack1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_defence1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_strength1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_hitpoints1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_ranged1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_prayer1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_magic1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_cooking1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_woodcutting1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_fletching1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_fishing1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_firemaking1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_crafting1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_smithing1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_mining1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_herblore1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_agility1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_thieving1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_slayer1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_farming1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_runecraft1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_hunter1.gif',
                 'https://www.runescape.com/img/rsp777/hiscores/skill_icon_construction1.gif',
                 'https://www.runescape.com/img/rsp777/game_icon_cluescrollsall.png',
                 'https://www.runescape.com/img/rsp777/game_icon_cluescrollsbeginner.png',
                 'https://www.runescape.com/img/rsp777/game_icon_cluescrollseasy.png',
                 'https://www.runescape.com/img/rsp777/game_icon_cluescrollsmedium.png',
                 'https://www.runescape.com/img/rsp777/game_icon_cluescroll',
                 'https://www.runescape.com/img/rsp777/rss.png']

    my_hook = Webhook(WHOOK)
    my_hook.send(test_list, "test", ignore_empty=True, formatting="*", items_per_request=3, delay=1)


if __name__ == '__main__':
    main()
