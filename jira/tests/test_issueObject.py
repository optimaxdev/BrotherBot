from unittest import TestCase

from jira.Objects import IssueObject


class TestIssueObject(TestCase):
    def test_properties(self):
        item = IssueObject(
            ident='ident1',
            key='key1',
            type='bug1',
            summary='summary1',
            due_date='due_date1',
            assignee='assignee1',
            project='project1',
            status='status1',
            host='host_jira'
        )
        self.assertEqual('ident1', item.ident)
        self.assertEqual('key1', item.key)
        self.assertEqual('bug1', item.type)
        self.assertEqual('summary1', item.summary)
        self.assertEqual('due_date1', item.due_date)
        self.assertEqual('assignee1', item.assignee)
        self.assertEqual('project1', item.project)
        self.assertEqual('status1', item.status)
        self.assertEqual('host_jira', item.host)
        self.assertEqual('host_jira/browse/key1', item.url)
        item.key = '1234'
        self.assertEqual('1234', item.key)
