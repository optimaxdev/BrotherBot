import datetime
from unittest import TestCase

from app.attendance.attendance_histogram import send_attendance_histogram


class TestSend_attendance_histogram(TestCase):
    def test_send_attendance_histogram(self):
        send_attendance_histogram(10, date=datetime.datetime.strptime("2019-03-06", "%Y-%m-%d"))
