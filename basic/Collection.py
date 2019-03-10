class Collection(dict):
    def __init__(self) -> None:
        super().__init__()
        self.collection = {}

    def add(self, key, value):
        self.collection[key] = value

    def get_collection(self) -> dict:
        return self.collection

    def get_length(self):
        return len(self.collection.items())

    def get_items(self):
        return self.collection.items()

    def get_values(self):
        return self.collection.values()

    def merge(self, collection):
        for key, value in collection.get_items():
            self.collection[key] = value
