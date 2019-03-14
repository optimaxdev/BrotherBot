from datetime import datetime
from unittest import TestCase

from Api import Api
from Objects import TimeObject, UserObject


class TestUser(TestCase):
    def test_create(self):
        user = UserObject(
            Api(),
            ident=1,
            name='test',
            discharge_date=datetime(2019, 1, 1)
        )
        self.assertEqual(1, user.ident)
        self.assertEqual('test', user.name)
        self.assertEqual(datetime(2019, 1, 1), user.discharge_date)

    def test_discharge_date_none(self):
        user = UserObject(Api())
        self.assertEqual(None, user.discharge_date)
        user.discharge_date = datetime(2019, 1, 1)
        self.assertEqual(datetime(2019, 1, 1), user.discharge_date)
        user.discharge_date = None
        self.assertEqual(None, user.discharge_date)

    def test_discharge_date_wrong_type(self):
        user = UserObject(Api())
        try:
            user.discharge_date = 'wrong-type'
        except TypeError:
            pass
        else:
            self.fail()

    def test_name(self):
        user = UserObject(Api())
        user.name = 'name'
        self.assertEqual('name', user.name)

    def test_get_time(self):
        user = UserObject(Api())
        self.assertEqual(TimeObject, type(user.time))
        time = TimeObject(1, Api())
        user.time = time
        self.assertEqual(time, user.time)
        try:
            user.time = 'wrong-type'
        except TypeError:
            pass
        else:
            self.fail()

    def test_is_fired(self):
        user = UserObject(Api())
        self.assertEqual(False, user.is_fired())
        user.discharge_date = datetime(2019, 1, 1)
        self.assertEqual(True, user.is_fired())
        user.discharge_date = None
        self.assertEqual(False, user.is_fired())
