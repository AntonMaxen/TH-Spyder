class Model:
    def __init__(self, base_url, source_url, login_url, root_element, unwanted_elements, hooks):
        self._model = {
            'base_url': base_url,
            'source_url': source_url,
            'login_url': login_url,
            'root_element': root_element,
            'unwanted_elements': unwanted_elements,
            'hooks': hooks
        }

    def __str__(self):
        return f"""
            'base_url': {self._model['base_url']}
            'source_url': {self._model['source_url']}
            'login_url' : {self._model['login_url']}
            'root_element': {self._model['root_element']}
            'unwanted_elements': {self._model['unwanted_elements']}
            'hooks': {self._model['hooks']}
        """


def main():
    my_model = Model(1, 2, 3, 4, 5, 6)
    print(my_model)
    pass


if __name__ == '__main__':
    main()
