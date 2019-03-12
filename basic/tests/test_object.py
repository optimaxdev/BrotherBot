from unittest import TestCase

from Object import Object


class TestObject(TestCase):
    def test_ident(self):
        item = Object()
        self.assertEqual(None, item.ident)
        item.ident = 'ident1'
        self.assertEqual('ident1', item.ident)

    def test_update(self):
        item = Object(
            ident='ident1'
        )
        self.assertEqual('ident1', item.ident)
