from unittest import TestCase

from Api import Api
from Objects import AttendanceObject


class TestAttendanceObject(TestCase):
    def test_api(self):
        api = Api()
        attendance = AttendanceObject(api)
        self.assertEqual(api, attendance.api)
        api2 = Api()
        attendance.api = api2
        self.assertEqual(api2, attendance.api)
