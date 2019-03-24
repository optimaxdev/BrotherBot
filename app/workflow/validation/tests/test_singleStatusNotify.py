from unittest import TestCase

from app.workflow.validation.singlestatus import SingleStatusNotify


class TestSingleStatusNotify(TestCase):
    def test_jql(self):
        notify = SingleStatusNotify(jql='project = WIN AND status in ("In Progress")')
        notify.report('slack', 'pmo_room_without_pmo')
