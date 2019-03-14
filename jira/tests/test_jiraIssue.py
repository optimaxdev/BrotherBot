import datetime
from unittest import TestCase

from jira.Objects import JiraIssue


class TestJiraIssue(TestCase):
    def test_properties(self):
        date = datetime.datetime.now()
        issue = JiraIssue(
            host='host1',
            ident='ident1',
            summary='summary1',
            key='key1',
            type='type1',
            due_date='111',
            assignee=11,
            project=22,
            status=33
        )
        self.assertEqual('ident1', issue.ident)
        self.assertEqual('host1', issue.host)
        self.assertEqual('summary1', issue.summary)
        self.assertEqual('key1', issue.key)
        self.assertEqual('type1', issue.type)
        self.assertEqual('111', issue.due_date)
        self.assertEqual(11, issue.assignee)
        self.assertEqual(22, issue.project)
        self.assertEqual(33, issue.status)
