import datetime
from unittest import TestCase

from app.attendance.absent import notify_absent_employees
from app.attendance.late import notify_late_employees


class TestNotify_absent_employees(TestCase):
    def test_notify_absent_employees(self):
        notify_absent_employees(datetime.datetime.now())

    def test_test(self):
        notify_late_employees(datetime.datetime.now())
