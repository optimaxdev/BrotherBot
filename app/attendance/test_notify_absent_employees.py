from datetime import datetime
from unittest import TestCase

from app.attendance.absent import notify_absent_employees


class TestNotify_absent_employees(TestCase):
    def test_notify_absent_employees(self):
        notify_absent_employees(datetime(2019, 3, 14), channel='pmo_room_without_pmo')
