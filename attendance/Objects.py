from datetime import datetime

from Api import get_employee_record_by_date
from Object import Object


class AttendanceTime:
    def __init__(self, user_id: str) -> None:
        super().__init__()
        self.timestamps = []
        self.user_id = user_id

    def load(self, date: datetime) -> None:
        for time in get_employee_record_by_date(self.user_id, date):
            self.timestamps.append(time)
        self.timestamps.sort()

    def get_date_records(self, date: datetime) -> list:
        records = [time for time in self.timestamps if time.date() == date.date()]
        if len(records) == 0:
            self.load(date)
            records = [time for time in self.timestamps if time.date() == date.date()]
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
        super().__init__()
        self._name = None
        self._discharge_date = None
        self.time = None
        self.update(kwargs)
        del kwargs
        self.update(locals())
        del self.self

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
        if not type(value) == datetime:
            raise TypeError("discharge_date value type must be datetime")
        self._discharge_date = value

    def is_fired(self):
        return self.discharge_date is not None

    def get_time(self) -> AttendanceTime:
        if self.time is None:
            self.time = AttendanceTime(self.ident)
        return self.time
