import requests

def main():
    url = "https://www.youtube.com"
    session = requests.session()
    req = session.get(url, headers=dict(referer=url))
    print(req)
    pass


if __name__ == '__main__':
    main()
