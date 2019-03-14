from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from Api import Api
from Objects import TimeObject


class TestTimeObject(TestCase):
    def create_mock_api(self):
        api_mock = Api()
        api_mock.get_employee_record_by_date = MagicMock(
            return_value=[datetime(2019, 1, 1, 0, 1, 1), datetime(2019, 1, 1, 0, 0, 1)]
        )
        return api_mock

    def test_user_id_property(self):
        time = TimeObject(1, self.create_mock_api())
        self.assertEqual(1, time.user_id)
        time.user_id = 2
        self.assertEqual(2, time.user_id)

    def test_get_date_records(self):
        api_mock = self.create_mock_api()
        time = TimeObject(1, api_mock)
        self.assertEqual(
            [datetime(2019, 1, 1, 0, 0, 1), datetime(2019, 1, 1, 0, 1, 1)],
            time.get_date_records(datetime(2019, 1, 1))
        )

    def test_get_first(self):
        api_mock = self.create_mock_api()
        time = TimeObject(1, api_mock)
        self.assertEqual(
            datetime(2019, 1, 1, 0, 0, 1),
            time.get_first(datetime(2019, 1, 1))
        )
        self.assertEqual(
            None,
            time.get_first(datetime(2019, 1, 2))
        )

    def test_get_last(self):
        api_mock = self.create_mock_api()
        time = TimeObject(1, api_mock)
        self.assertEqual(
            datetime(2019, 1, 1, 0, 1, 1),
            time.get_last(datetime(2019, 1, 1))
        )
        self.assertEqual(
            None,
            time.get_first(datetime(2019, 1, 2))
        )

    def test_is_absent(self):
        api_mock = self.create_mock_api()
        time = TimeObject(1, api_mock)
        self.assertEqual(
            True,
            time.is_absent(datetime(2019, 1, 2))
        )
        self.assertEqual(
            False,
            time.is_absent(datetime(2019, 1, 1))
        )
