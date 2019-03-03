import datetime
from unittest import TestCase

from attendance.bosscontrol import BosscontrolApi


class TestBosscontrolApi(TestCase):
    def test_get_employees_list(self):
        BosscontrolApi().get_employees_list()

    def test_get_employee_records_by_date(self):
        BosscontrolApi().get_employee_records_by_date(datetime.datetime.now())
