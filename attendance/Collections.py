import datetime

from Api import get_employee_list
from Objects import User
from basic.Collection import Collection


class UserCollection(Collection):
    def load_users(self):
        for employee_data in get_employee_list():
            self.add(User(
                ident=employee_data['code'],
                name=employee_data['name'],
                discharge_date=employee_data['discharge_date']
            ))

    def get_absent_list(self, date: datetime) -> list:
        return [user for user in self.get_list() if user.get_time().is_absent(date)]

    def get_late_list(self, date: datetime, start_work_hour: int, reverse=True) -> list:
        user_is_late = []

        for user in self.get_list():
            time = user.get_time()
            if time.is_absent(date):
                continue
            if time.get_first(date).hour >= start_work_hour and time.get_first(date).minute > 0:
                user_is_late.append(user)

        return sorted(user_is_late, key=lambda k: k.get_attendance().get_first(date), reverse=reverse)
