from unittest import TestCase

from app.jiraissues import check_issue_unique


class TestCheck_issue_unique(TestCase):
    def test_check_issue_unique(self):
        check_issue_unique()
