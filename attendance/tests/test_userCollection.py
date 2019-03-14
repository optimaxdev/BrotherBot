from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from Api import Api
from attendance.Collections import UserCollection


class TestUserCollection(TestCase):

    def create_mock_api(self):
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
                    'discharge_date': datetime(2019, 1, 1, 10, 1, 0)
                },
                {
                    'code': 'test3',
                    'name': 'name3',
                    'discharge_date': None
                },
            ]
        )
        api_mock.get_employee_record_by_date = MagicMock(
            return_value=[
                datetime(2019, 1, 1, 0, 1, 1),
                datetime(2019, 1, 1, 0, 0, 1)
            ]
        )
        return api_mock

    def test_get_list(self):
        collection = UserCollection(api=self.create_mock_api())
        self.assertEqual(3, collection.get_length())
        self.assertEqual('name1', collection.get('test1').name)
        self.assertEqual(None, collection.get('test1').discharge_date)

    def test_get_absent_list(self):
        collection = UserCollection(api=self.create_mock_api())

        late_list = collection.get_late_list(datetime(2019, 1, 1), 10, reverse=True)
        self.assertEqual(1, len(late_list))
        self.assertEqual([user1], late_list)
