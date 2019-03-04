import datetime
from unittest import TestCase

from attendance.bosscontrol import load_employees, load_attendance_time


class TestBosscontrolApi(TestCase):
    def test_get_employees_list(self):
        BosscontrolApi().get_employees_list()

    def test_get_employee_records_by_date(self):
        BosscontrolApi().get_employee_records_by_date(datetime.datetime.now())

    def test_funct(self):
        collection = load_employees()
        load_attendance_time(collection, datetime.datetime.now())
        collection.get_collection()
