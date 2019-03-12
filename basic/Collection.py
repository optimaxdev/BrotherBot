from Object import Object


class Collection(dict):
    def __init__(self) -> None:
        super().__init__()
        self.collection = {}

    def add(self, value: Object):
        self.collection[value.ident] = value

    def get_length(self):
        return len(self.collection.items())

    def get_items(self):
        return self.collection.items()

    def get_list(self):
        return list(self.collection.values())

    def get(self, key):
        return self.collection.get(key)

    def merge(self, collection):
        for key, value in collection.get_items():
            self.collection[key] = value
