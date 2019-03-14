from datetime import datetime

from Api import Api
from Object import Object


class AttendanceTime:
    def __init__(self, user_id, api=None) -> None:
        super().__init__()
        self._timestamps = []
        self._user_id = user_id
        self._api = api

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def api(self):
        if self._api is None:
            self._api = Api()
        return self._api

    @api.setter
    def api(self, value):
        if type(value) != Api:
            raise TypeError("api value type must be Api")
        self._api = value

    def get_date_records(self, date: datetime) -> list:
        records = [time for time in self._timestamps if time.date() == date.date()]
        if len(records) == 0:
            for time in self.api.get_employee_record_by_date(self.user_id, date):
                self._timestamps.append(time)
            self._timestamps.sort()
            records = [time for time in self._timestamps if time.date() == date.date()]
        return records

    def get_first(self, date: datetime) -> datetime:
        records = self.get_date_records(date)
        records.sort(reverse=False)
        return records[0] if len(records) > 0 else None

    def get_last(self, date: datetime):
        records = self.get_date_records(date)
        records.sort(reverse=True)
        return records[0] if len(records) > 0 else None

    def is_absent(self, date: datetime) -> bool:
        return len(self.get_date_records(date)) == 0


class User(Object):
    def __init__(self, **kwargs) -> None:
        self._name = kwargs['name'] if 'name' in kwargs else None
        self._discharge_date = kwargs['discharge_date'] if 'discharge_date' in kwargs else None
        self._time = kwargs['time'] if 'time' in kwargs else None
        self._api = kwargs['api'] if 'api' in kwargs else None
        super().__init__(**kwargs)
        self.update(kwargs)
        del kwargs
        self.update(locals())
        del self.self

    @property
    def api(self):
        if self._api is None:
            self._api = Api()
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def discharge_date(self):
        return self._discharge_date

    @discharge_date.setter
    def discharge_date(self, value):
        if type(value) != datetime and value is not None:
            raise TypeError("discharge_date value type must be datetime or None")
        self._discharge_date = value

    @property
    def time(self):
        if self._time is None:
            self._time = AttendanceTime(self.ident, api=self.api)
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    def is_fired(self):
        return self.discharge_date is not None
