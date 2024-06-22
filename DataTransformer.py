class DataTransformer:
    def add_prefix(self, prefix: str, data: list):
        return list(map(lambda item: prefix + str(item), data))
