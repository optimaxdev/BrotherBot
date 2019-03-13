from unittest import TestCase

import httpretty as httpretty

from Api import *


class TestApi(TestCase):

    @httpretty.activate
    def test_get_employee_list_by_department_bad_response(self):
        httpretty.register_uri(httpretty.POST, Config.ATTENDANCE_BOSSCONTROL_HOST, body="Bad json string")
        self.assertEqual([], get_employee_list_by_department('department_test', datetime.now()))

    @httpretty.activate
    def test_get_employee_list_by_department_no_results(self):
        httpretty.register_uri(httpretty.POST, Config.ATTENDANCE_BOSSCONTROL_HOST, body="{\"no\": \"results\"}")
        self.assertEqual([], get_employee_list_by_department('department_test', datetime.now()))

    @httpretty.activate
    def test_get_employee_list_by_department(self):
        httpretty.register_uri(
            httpretty.POST,
            Config.ATTENDANCE_BOSSCONTROL_HOST,
            body="{\"result\": [{\"id\": \"1\"}]}"
        )
        self.assertEqual([{'id': '1'}], get_employee_list_by_department('department_test', datetime.now()))

    @httpretty.activate
    def test_get_employee_list_ignore(self):
        httpretty.register_uri(
            httpretty.POST,
            Config.ATTENDANCE_BOSSCONTROL_HOST,
            body="{\"result\": [{\"code\": \"1\"}]}"
        )
        Config.ATTENDANCE_DEPARTMENT = ['only-one']
        Config.ATTENDANCE_USER_IGNORE = ['1']
        self.assertEqual([], get_employee_list())

    @httpretty.activate
    def test_get_employee_list(self):
        httpretty.register_uri(
            httpretty.POST,
            Config.ATTENDANCE_BOSSCONTROL_HOST,
            body="{\"result\": [{\"code\": \"1\"}]}"
        )
        Config.ATTENDANCE_DEPARTMENT = ['only-one']
        Config.ATTENDANCE_USER_IGNORE = []
        self.assertEqual([{'code': '1'}], get_employee_list())

    @httpretty.activate
    def test_get_employee_list_wrong_format(self):
        httpretty.register_uri(
            httpretty.POST,
            Config.ATTENDANCE_BOSSCONTROL_HOST,
            body="{\"result\": [{\"no-code\": \"1\"}]}"
        )
        Config.ATTENDANCE_DEPARTMENT = ['only-one']
        Config.ATTENDANCE_USER_IGNORE = []
        self.assertEqual([], get_employee_list())

    @httpretty.activate
    def test_get_employee_record_by_date_bad_response(self):
        httpretty.register_uri(httpretty.POST, Config.ATTENDANCE_BOSSCONTROL_HOST, body="Bad json string")
        self.assertEqual([], get_employee_record_by_date('employee_id', datetime.now()))

    @httpretty.activate
    def test_get_employee_record_by_date_no_results(self):
        httpretty.register_uri(httpretty.POST, Config.ATTENDANCE_BOSSCONTROL_HOST, body="{\"no\": \"results\"}")
        self.assertEqual([], get_employee_record_by_date('employee_id', datetime.now()))

    @httpretty.activate
    def test_get_employee_record_by_date(self):
        httpretty.register_uri(
            httpretty.POST,
            Config.ATTENDANCE_BOSSCONTROL_HOST,
            body="{\"result\": [{\"timestamp\": \"2019-01-01 00:00:00\"}, {\"wrong-name\": \"2019-01-01 00:00:00\"}]}"
        )
        self.assertEqual(
            [datetime(2019, 1, 1, 0, 0)],
            get_employee_record_by_date('employee_id', datetime.now())
        )
