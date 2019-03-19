from unittest import TestCase

from app.workflow.validation.noassignee import check_no_assignee


class TestApi(TestCase):
    def test_search(self):
        check_no_assignee('status in ("To Do", Testing, "Code Review", "In Development", "Create Checklist", '
                          '"Write Test Cases") AND assignee in (EMPTY) ')
