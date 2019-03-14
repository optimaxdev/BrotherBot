from datetime import datetime

from attendance.Api import Api
from basic.Object import Object


class AttendanceObject(Object):
    def __init__(self, api: Api, **kwargs) -> None:
        super().__init__(**kwargs)
        self._api = api

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        self._api = value


class TimeObject(AttendanceObject):
    def __init__(self, user_id, api: Api, **kwargs) -> None:
        super().__init__(api, **kwargs)
        self._timestamps = []
        self._user_id = user_id

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

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


class UserObject(AttendanceObject):
    def __init__(self, api: Api, **kwargs) -> None:
        super().__init__(api, **kwargs)
        self._name = kwargs['name'] if 'discharge_date' in kwargs else None
        self._discharge_date = kwargs['discharge_date'] if 'discharge_date' in kwargs else None
        if self._discharge_date == '':
            self._discharge_date = None
        self._time = kwargs['time'] if 'time' in kwargs else None

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
            self._time = TimeObject(self.ident, self.api)
        return self._time

    @time.setter
    def time(self, value):
        if type(value) != TimeObject:
            raise TypeError("time value type must be TimeObject")
        self._time = value

    def is_fired(self):
        return self.discharge_date is not None
