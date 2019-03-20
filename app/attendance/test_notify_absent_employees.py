from unittest import TestCase

from app.workflow.validation.duedate import check_due_date


class TestNotify_absent_employees(TestCase):
    def test_notify_absent_employees(self):
        check_due_date(
            'project in (GUSA, OPT) AND status in ("In Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is EMPTY)',
            channel='pmo_room_without_pmo'
        )
