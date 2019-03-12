from unittest import TestCase

from Object import Object
from basic.Collection import Collection


class TestCollection(TestCase):
    def test_add_and_get_items(self):
        collection = Collection()
        obj = Object(ident=1, name='test')
        self.assertEqual(0, collection.get_length())
        self.assertEqual({}, dict(collection.get_items()))
        collection.add(obj)
        self.assertEqual(1, collection.get_length())
        self.assertEqual({1: obj}, dict(collection.get_items()))

    def test_get_length(self):
        collection = Collection()
        self.assertEqual(0, collection.get_length())
        collection.add(Object(ident=1, name='test'))
        self.assertEqual(1, collection.get_length())

    def test_get_list(self):
        collection = Collection()
        self.assertEqual([], list(collection.get_list()))
        obj1 = Object(ident='1', name='test1')
        obj2 = Object(ident='2', name='test2')
        collection.add(obj1)
        collection.add(obj2)
        self.assertEqual([obj1, obj2], list(collection.get_list()))

    def test_merge(self):
        obj1 = Object(ident='1', name='test1')
        obj2 = Object(ident='2', name='test2')
        obj3 = Object(ident='2', name='test3')

        collection1 = Collection()
        collection1.add(obj1)
        collection1.add(obj2)

        collection2 = Collection()
        collection2.add(obj3)

        collection1.merge(collection2)
        self.assertEqual({'1': obj1, '2': obj3}, dict(collection1.get_items()))

    def test_get(self):
        collection = Collection()
        obj = Object(ident='1', name='test')
        self.assertEqual(None, collection.get('1'))
        collection.add(obj)
        self.assertEqual(obj, collection.get('1'))
