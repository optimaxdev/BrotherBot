from unittest import TestCase

from basic.Collection import Collection


class TestCollection(TestCase):
    def test_add_and_get_items(self):
        collection = Collection()
        self.assertEqual(0, collection.get_length())
        self.assertEqual({}, dict(collection.get_items()))
        collection.add('1', 'test')
        self.assertEqual(1, collection.get_length())
        self.assertEqual({'1': 'test'}, dict(collection.get_items()))

    def test_get_collection(self):
        collection = Collection()
        self.assertEqual({}, dict(collection.get_items()))
        collection.add('1', 'test')
        self.assertEqual({'1': 'test'}, dict(collection.get_items()))

    def test_get_length(self):
        collection = Collection()
        self.assertEqual(0, collection.get_length())
        collection.add('1', 'test')
        self.assertEqual(1, collection.get_length())

    def test_get_list(self):
        collection = Collection()
        self.assertEqual([], list(collection.get_list()))
        collection.add('1', 'test1')
        collection.add('2', 'test2')
        self.assertEqual(['test1', 'test2'], list(collection.get_list()))

    def test_merge(self):
        collection1 = Collection()
        collection1.add('1', 'test1')
        collection1.add('2', 'test_off')
        collection2 = Collection()
        collection2.add('2', 'test2')

        collection1.merge(collection2)
        self.assertEqual({'1': 'test1', '2': 'test2'}, dict(collection1.get_items()))
