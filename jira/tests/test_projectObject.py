from unittest import TestCase

from jira.Objects import ProjectObject


class TestProjectObject(TestCase):
    def test_properties(self):
        item = ProjectObject(
            ident='ident1',
            name='display_name1'
        )
        self.assertEqual('ident1', item.ident)
        self.assertEqual('display_name1', item.name)
