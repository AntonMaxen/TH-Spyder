import json


def main():
    with open("thspyder/models/models.json") as json_file:
        data = json.load(json_file)
        for item in data:
            for key, value in item.items():
                if key == "login":
                    auth_func = value['auth_func']
                    my_func = create_function_from_string(auth_func)
                    print(my_func(11))


def create_function_from_string(string):
    if string is None:
        return None

    if 'lambda' in string:
        string = f'func = {string}'
    loc = {}
    exec(string, {}, loc)
    funcs = [loc.get(func, None) for func in loc.keys()]
    return funcs[0] if len(funcs) > 0 else None


if __name__ == '__main__':
    main()
