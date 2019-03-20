from datetime import datetime
from unittest import TestCase

from app.workflow.validation.singlestatus import check_single_status


class TestNotify_absent_employees(TestCase):
    def test_notify_absent_employees(self):
        check_single_status(
            'project in (UVP, BAC, BUG, GRO, ANT, GD, OPT, OT) AND issuetype in (Bug, Improvement, '
            '"New Feature", QA, Story, Task) AND status in ("In Progress", Testing, "Code Review", '
            '"Create Checklist", "Write Test Cases")',
            channel='pmo_room_without_pmo'
        )
