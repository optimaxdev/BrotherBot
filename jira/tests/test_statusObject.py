from unittest import TestCase

from jira.Objects import StatusObject


class TestStatusObject(TestCase):
    def test_properties(self):
        item = StatusObject(
            ident='ident1',
            name='display_name1'
        )
        self.assertEqual('ident1', item.ident)
        self.assertEqual('display_name1', item.name)
