from unittest import TestCase

from jira.Collections import IssueCollection
from jira.api import JiraIssue


class TestIssueCollection(TestCase):
    def test_add_issue(self):
        issue = JiraIssue({'id': 'issue1'})
        collection = IssueCollection()
        collection.add_issue(issue)
        self.assertEqual(issue, collection.get('issue1'))
