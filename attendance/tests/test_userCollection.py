import datetime
from unittest import TestCase

from attendance.Collections import UserCollection


class TestUserCollection(TestCase):
    def test_get_absent_list(self):
        absent_date = datetime.datetime.now()

        user1 = AttendanceUser({'code': 'code1'})
        user1.get_attendance().add(absent_date)
        user2 = AttendanceUser({'code': 'absent_user'})

        collection = UserCollection()
        collection.add_user(user1)
        collection.add_user(user2)

        self.assertEqual(1, len(collection.get_absent_list(absent_date)))
        self.assertEqual('absent_user', collection.get_absent_list(absent_date)[0].get_id())

    def test_get_late_list(self):
        late_time1 = datetime.datetime(2019, 1, 1, 10, 1, 0)
        late_time2 = datetime.datetime(2019, 1, 1, 10, 1, 1)
        good_time1 = datetime.datetime(2019, 1, 1, 10, 0, 0)
        good_time2 = datetime.datetime(2019, 1, 1, 9, 59, 59)

        user1 = AttendanceUser({'code': 'late_user'})
        user1.get_attendance().add(late_time1)
        user1 = AttendanceUser({'code': 'late_user'})
        user1.get_attendance().add(late_time1)
        user2 = AttendanceUser({'code': 'good_user1'})
        user2.get_attendance().add(good_time1)
        user3 = AttendanceUser({'code': 'good_user2'})
        user3.get_attendance().add(good_time2)
        user4 = AttendanceUser({'code': 'all_in_one'})
        user4.get_attendance().add(late_time)
        user4.get_attendance().add(good_time1)
        user4.get_attendance().add(good_time2)

        collection = UserCollection()
        collection.add_user(user1)
        collection.add_user(user2)
        collection.add_user(user3)
        collection.add_user(user4)

        late_list = collection.get_late_list(datetime.datetime(2019, 1, 1), 10, reverse=True)
        self.assertEqual(1, len(late_list))
        self.assertEqual([user1], late_list)

    def test_add_user(self):
        user1 = AttendanceUser({'code': 'added_user'})

        collection = UserCollection()
        collection.add_user(user1)

        self.assertEqual(1, len(collection.get_list()))
        self.assertEqual(user1, collection.get('added_user'))
