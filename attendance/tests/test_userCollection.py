from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from attendance.Api import Api
from attendance.Collections import UserCollection


class TestUserCollection(TestCase):

    def create_mock_api(self):
        def record_side_effect(employee_id: str, date: datetime):
            if employee_id == 'test1':
                return [
                    datetime(2019, 1, 1, 10, 9, 59),
                    datetime(2019, 1, 1, 10, 0, 0),
                    datetime(2019, 1, 1, 10, 0, 1),
                    datetime(2019, 1, 2, 10, 0, 2),
                    datetime(2019, 1, 2, 10, 0, 1)
                ]
            if employee_id == 'test2':
                return [
                    datetime(2019, 1, 1, 10, 0, 1),
                    datetime(2019, 1, 2, 10, 0, 2),
                ]
            if employee_id == 'test3':
                return [
                    datetime(2019, 1, 2, 10, 0, 1)
                ]
            if employee_id == 'test4':
                return [
                    datetime(2019, 1, 2, 10, 0, 0),
                    datetime(2019, 1, 3, 10, 0, 0)
                ]

        api_mock = Api()
        api_mock.get_employee_list = MagicMock(
            return_value=[
                {
                    'code': 'test1',
                    'name': 'name1'
                },
                {
                    'code': 'test2',
                    'name': 'name2',
                    'discharge_date': datetime(2018, 1, 1, 10, 1, 0)
                },
                {
                    'code': 'test3',
                    'name': 'name3',
                    'discharge_date': None
                },
                {
                    'code': 'test4',
                    'name': 'name4',
                }
            ]
        )
        api_mock.get_employee_record_by_date = MagicMock(side_effect=record_side_effect)
        return api_mock

    def test_api_property(self):
        api = self.create_mock_api()
        collection = UserCollection(api=api)
        self.assertEqual(api, collection.api)
        api2 = self.create_mock_api()
        collection.api = api2
        self.assertEqual(api2, collection.api)

    def test_get_list(self):
        collection = UserCollection(api=self.create_mock_api())
        self.assertEqual(4, collection.get_length())
        self.assertEqual('name1', collection.get('test1').name)
        self.assertEqual(None, collection.get('test1').discharge_date)

    def test_get_absent_list(self):
        collection = UserCollection(api=self.create_mock_api())
        self.assertEqual(['test3', 'test4'], [user.ident for user in collection.get_absent_list(datetime(2019, 1, 1))])
        self.assertEqual([], [user.ident for user in collection.get_absent_list(datetime(2019, 1, 2))])

    def test_get_late_list(self):
        collection = UserCollection(api=self.create_mock_api())
        self.assertEqual(
            [],
            [user.ident for user in collection.get_late_list(datetime(2019, 1, 1, 1, 1, 1), 10, True)]
        )
        self.assertEqual(
            ['test1', 'test3'],
            [user.ident for user in collection.get_late_list(datetime(2019, 1, 2, 1, 1, 1), 10, False)]
        )
