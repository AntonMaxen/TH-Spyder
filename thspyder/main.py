from thspyder.spider import Spider
from thspyder.models import model_wiki, model_rs, model_wiki_random, default_model
from thspyder.model_pp import modelpp
from thspyder.processor import DataProcessor, difference, list_difference
import thspyder.helpers.myconstants as constants

import requests
import json
WHOOK = "https://discordapp.com/api/webhooks/769671953438343178/YFzZmckeAL1Lhw9YXJVlWuvMyhGOEWyQ-3CsofcRHNmWjmrwBSRKN4kxq3CfgWPfSp_L"


def main():
    rs_spider = Spider(model_rs)
    name = model_rs['name']
    rs_spider.run()
    rs_processor = DataProcessor((constants.STORAGE_FOLDER, constants.DATA_FOLDER), name)
    dict_list = rs_processor.file_dicts()
    diff_list = difference(dict_list)
    for folder_name in diff_list.keys():
        for filename, changes in diff_list[folder_name].items():
            if folder_name == constants.TEXT_FOLDER:
                data = {
                    "content": "\n".join([f'``{change}``' for change in changes]),
                    "username": filename
                }
                result = requests.post(WHOOK, data=json.dumps(data), headers={"Content-Type": "application/json"})
                print(filename)
                print(changes)


if __name__ == '__main__':
    main()
