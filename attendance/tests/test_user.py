from datetime import datetime
from unittest import TestCase

from Objects import User, AttendanceTime


class TestUser(TestCase):
    def test_create(self):
        user = User(
            ident=1,
            name='test',
            discharge_date=datetime(2019, 1, 1)
        )
        self.assertEqual(1, user.ident)
        self.assertEqual('test', user.name)
        self.assertEqual(datetime(2019, 1, 1), user.discharge_date)

    def test_discharge_date_none(self):
        user = User()
        self.assertEqual(None, user.discharge_date)
        user.discharge_date = datetime(2019, 1, 1)
        self.assertEqual(datetime(2019, 1, 1), user.discharge_date)
        user.discharge_date = None
        self.assertEqual(None, user.discharge_date)

    def test_discharge_date_wrong_type(self):
        user = User()
        try:
            user.discharge_date = 'wrong-type'
        except TypeError:
            pass
        else:
            self.fail()

    def test_get_time(self):
        user = User()
        self.assertEqual(AttendanceTime, type(user.get_time()))
        time = user.get_time()
        self.assertEqual(time, user.get_time())

    def test_is_fired(self):
        user = User()
        self.assertEqual(False, user.is_fired())
        user.discharge_date = datetime(2019, 1, 1)
        self.assertEqual(True, user.is_fired())
        user.discharge_date = None
        self.assertEqual(False, user.is_fired())
