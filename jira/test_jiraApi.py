from unittest import TestCase

from jira.api import JiraApi, DEFAULT_UVP_JQL


class TestJiraApi(TestCase):
    def test_search(self):
        JiraApi().search(DEFAULT_UVP_JQL)
