import os
import pickle
import re
from urllib.parse import urlparse
from pathlib import Path
from thspyder.helpers.helper import get_project_root

def main():
    url = "https://www.pingpong.se/pp/courses/course11264//published/1603355279043/resourceId/4590211/content/d8def78c-953c-41d7-a219-7d16ae3b73c1/93637585-7e1f-40cc-b8a0-4ec2681bc074.html"
    uri = urlparse(url)
    folder = "p"
    filename = f'{os.path.basename(uri.path)}.pickle'

    root = get_project_root()
    parent_dir = os.path.normpath(root)

    urlpath = os.path.dirname(uri.path)
    clean_urlpath = [p for p in re.split('(/+)', urlpath) if p and not re.match('(/+)', p)]

    path = os.path.join(parent_dir, folder, uri.netloc, *clean_urlpath)
    fullpath = os.path.join(path, filename)
    print(fullpath)


    Path(path).mkdir(parents=True, exist_ok=True)
    with open(fullpath, 'wb+') as p_file:
        pickle.dump(filename, p_file)



if __name__ == '__main__':
    main()
