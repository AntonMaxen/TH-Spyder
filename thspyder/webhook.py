import requests
import json
import time
MAX_UNICODE_CHARS = 2000


class Webhook:
    """Class Webhook is a integration for discords webhook api,
    it sends json data to discords api so it can be viewed in discord"""
    def __init__(self, url, **webhook_config):
        self.url = url
        self.ignore_empty = webhook_config.get("ignore_empty", False)
        self.formatting = webhook_config.get("formatting", "")
        self.items_per_request = webhook_config.get("items_per_request", 0)
        self.delay = webhook_config.get("delay", 2)
        self.timestamp = webhook_config.get("timestamp", False)

    def send(self, content, name):
        if self.ignore_empty:
            content = [line for line in content if line]

        username = f'{str(round(time.time()))}: {name}' if self.timestamp else name
        # add formatting
        content = [f'{self.formatting}{line}{self.formatting}' if line else line for line in content]
        # split lists for separate requests
        list_of_requests = split_list_in_requests(content, self.items_per_request)
        splitted_content = [split_list(content, MAX_UNICODE_CHARS) for content in list_of_requests]

        for list_content in splitted_content:
            for c in list_content:
                data = {
                    "content": "\n".join(c),
                    "username": username
                }

                result = requests.post(self.url, data=json.dumps(data), headers={"Content-Type": "application/json"})

                try:
                    result.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    print(err)
                else:
                    print("success")

                if len(list_content) > 1 or len(splitted_content) > 1:
                    time.sleep(self.delay)


def split_list(my_list, max_chars):
    """splits a list in lists if num_characters in list is > max_chars"""
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


def split_list_in_requests(my_list, items_per_request):
    """divides list in groups of x: items_per_request"""
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
