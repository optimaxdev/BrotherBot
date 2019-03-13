from datetime import datetime
from unittest import TestCase
import httpretty

from Objects import AttendanceTime
from config import Config


class TestAttendanceTime(TestCase):

    @httpretty.activate
    def test_get_date_records(self):
        httpretty.register_uri(
            httpretty.POST,
            Config.ATTENDANCE_BOSSCONTROL_HOST,
            body="{\"result\": [{\"timestamp\": \"2019-01-01 00:01:01\"},{\"timestamp\": \"2019-01-01 00:00:01\"}]}"
        )
        time = AttendanceTime(1)
        self.assertEqual(
            [datetime(2019, 1, 1, 0, 0, 1), datetime(2019, 1, 1, 0, 1, 1)],
            time.get_date_records(datetime(2019, 1, 1))
        )

    @httpretty.activate
    def test_get_first(self):
        httpretty.register_uri(
            httpretty.POST,
            Config.ATTENDANCE_BOSSCONTROL_HOST,
            body="{\"result\": [{\"timestamp\": \"2019-01-01 00:01:01\"},{\"timestamp\": \"2019-01-01 00:00:01\"}]}"
        )
        time = AttendanceTime(1)
        self.assertEqual(
            datetime(2019, 1, 1, 0, 0, 1),
            time.get_first(datetime(2019, 1, 1))
        )

    @httpretty.activate
    def test_get_last(self):
        httpretty.register_uri(
            httpretty.POST,
            Config.ATTENDANCE_BOSSCONTROL_HOST,
            body="{\"result\": [{\"timestamp\": \"2019-01-01 00:01:01\"},{\"timestamp\": \"2019-01-01 00:00:01\"}]}"
        )
        time = AttendanceTime(1)
        self.assertEqual(
            datetime(2019, 1, 1, 0, 1, 1),
            time.get_last(datetime(2019, 1, 1))
        )

    @httpretty.activate
    def test_is_absent_true(self):
        httpretty.register_uri(
            httpretty.POST,
            Config.ATTENDANCE_BOSSCONTROL_HOST,
            body="{\"result\": []}"
        )
        time = AttendanceTime(1)
        self.assertEqual(
            True,
            time.is_absent(datetime(2019, 1, 1))
        )

    @httpretty.activate
    def test_is_absent_false(self):
        httpretty.register_uri(
            httpretty.POST,
            Config.ATTENDANCE_BOSSCONTROL_HOST,
            body="{\"result\": [{\"timestamp\": \"2019-01-01 00:01:01\"},{\"timestamp\": \"2019-01-01 00:00:01\"}]}"
        )
        time = AttendanceTime(1)
        self.assertEqual(
            False,
            time.is_absent(datetime(2019, 1, 1))
        )
