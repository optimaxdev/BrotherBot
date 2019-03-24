from unittest import TestCase

from app.workflow.validation.noassignee import NoAssigneeNotify


class TestNoAssigneeNotify(TestCase):
    def test_jql(self):
        item = NoAssigneeNotify()
        self.assertEqual(None, item.jql)
        item.jql = 'test'
        self.assertEqual('test', item.jql)
