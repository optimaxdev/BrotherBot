from unittest import TestCase

from app.workflow.validation.duedate import check_due_date


class TestCheck_single_status(TestCase):
    def test_check_single_status(self):
        check_due_date('project in (GUSA, GRO, BUG, OPT, ANT, BAC, GD, OT, UVP) AND status in ("In Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases")', 'pmo_room_without_pmo')
