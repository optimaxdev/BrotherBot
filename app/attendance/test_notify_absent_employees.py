from datetime import datetime
from unittest import TestCase

from app.attendance.late import notify_late_employees


class TestNotify_absent_employees(TestCase):
    def test_notify_absent_employees(self):
        notify_late_employees(datetime(2019, 3, 19), channel='pmo_room_without_pmo')
