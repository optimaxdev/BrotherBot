import datetime

from Api import Api
from Objects import User
from basic.Collection import Collection


class UserCollection(Collection):
    def __init__(self, api=Api()) -> None:
        super().__init__()
        self._api = api
        self._load_users()

    @property
    def api(self):
        if self._api is None:
            self._api = Api()
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

    def _load_users(self):
        for employee_data in self._api.get_employee_list():
            self.add(User(
                ident=employee_data['code'],
                name=employee_data['name'],
                discharge_date=employee_data['discharge_date'] if 'discharge_date' in employee_data else None,
                api=self.api
            ))

    def get_absent_list(self, date: datetime) -> list:
        return [user for user in self.get_list() if user.time.is_absent(date)]

    def get_late_list(self, date: datetime, start_work_hour: int, reverse=True) -> list:
        user_is_late = []

        for user in self.get_list():
            time = user.time
            if time.is_absent(date):
                continue
            if time.get_first(date).hour >= start_work_hour and time.get_first(date).minute > 0:
                user_is_late.append(user)

        return sorted(user_is_late, key=lambda k: k.time.get_first(date), reverse=reverse)
