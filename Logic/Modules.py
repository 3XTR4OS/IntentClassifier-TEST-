class LocalStorage:
    def __init__(self):
        self.__data = None

    def save(self, data):
        self.__data = data

    def get_data(self):
        return self.__data


