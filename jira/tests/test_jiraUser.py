from unittest import TestCase

from jira.Objects import JiraUser


class TestJiraUser(TestCase):
    def test_properties(self):
        user = JiraUser(
            ident='ident1',
            email='email1',
            display_name='display_name1'
        )
        self.assertEqual('ident1', user.ident)
        self.assertEqual('email1', user.email)
        self.assertEqual('display_name1', user.display_name)
