import datetime
import json

import requests

from basic.Collection import Collection
from config import Config


WORKING_TIME_START = 10
WORKING_TIME_FINISH = 19


class AttendanceTime:
    def __init__(self) -> None:
        super().__init__()
        self.timestamps = []

    def add(self, date: datetime):
        self.timestamps.append(date)

    def sort(self, reverse=False):
        self.timestamps.sort(reverse=reverse)

    def get_first(self, date=datetime.datetime.now()):
        first_time_date = None
        for time in self.timestamps:
            if time.date() != date.date():
                continue
            if first_time_date is None:
                first_time_date = time
                continue
            if first_time_date > time:
                first_time_date = time
        return first_time_date

    def get_last(self, date=datetime.datetime.now()):
        first_time_date = None
        for time in self.timestamps:
            if time.date() != date.date():
                continue
            if first_time_date is None:
                first_time_date = time
                continue
            if first_time_date < time:
                first_time_date = time
        return first_time_date

    def is_absent(self, date=datetime.datetime.now()):
        is_absent = True
        for time in self.timestamps:
            if time.date() == date.date():
                is_absent = False
        return is_absent


class AttendanceUser:
    def __init__(self, data) -> None:
        super().__init__()
        self.data = data
        self.time = AttendanceTime()

    def get_id(self):
        return self.data['code']

    def get_name(self):
        return self.data['name']

    def get_discharge_date(self):
        return self.data['discharge_date']

    def is_fired(self):
        return self.get_discharge_date() is not None

    def get_attendance(self) -> AttendanceTime:
        return self.time


class AttendanceCollection(Collection):
    def get_absent_employees(self, date=datetime.datetime.now()) -> list:
        result = []
        for user in self.collection.values():
            if user.get_attendance().is_absent(date):
                result.append(user)
        return result

    def get_late_rate_list(self, date: datetime) -> list:
        user_is_late = []
        for user in self.collection.values():
            attendance = user.get_attendance()
            if not attendance.is_absent(date) and attendance.get_first(date).hour >= 10:
                user_is_late.append(user)
        return sorted(user_is_late, key=lambda k: k.get_attendance().get_first(date), reverse=True)


class BosscontrolApi:
    """
    Documentation is here https://www.bosscontrol.ru/api/docs/
    """
    def __init__(self):
        self.username = Config().ATTENDANCE_BOSSCONTROL_USERNAME
        self.password = Config().ATTENDANCE_BOSSCONTROL_PASSWORD
        self.host = "https://www.bosscontrol.ru/timeattendance/json/"

    def get_employee_list_by_department(self, department_id) -> list:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        response = requests.post(self.host, json={
            'id': 'request_id',
            'method': 'timeattendance.getDepartmentEmployeesForPeriod',
            'params': [self.username, self.password, department_id, current_date, current_date]
        })
        return json.loads(response.text)['result']

    def get_employee_record_by_date(self, employee_id: str, date: datetime) -> list:
        response = requests.post(self.host, json={
            'id': 'request_id',
            'method': 'timeattendance.getEmployeeRecords',
            'params': [self.username, self.password, employee_id, date.strftime("%Y-%m-%d")]
        })

        result = []
        for attendance in json.loads(response.text)['result']:
            result.append(datetime.datetime.strptime(attendance['timestamp'], '%Y-%m-%d %H:%M:%S'))

        return result


def load_employees():
    department_list = [
        "bosscontrol_internal_grp_15355",
        "bosscontrol_internal_grp_15359",
        "bosscontrol_internal_grp_15356",
        "bosscontrol_internal_grp_15357",
        "bosscontrol_internal_grp_15358"
    ]
    employee_ignore = [
        'bosscontrol_internal_801591',
        'bosscontrol_internal_765085'
    ]

    collection = AttendanceCollection()
    for department_id in department_list:
        employee_list = BosscontrolApi().get_employee_list_by_department(department_id)
        for employee_data in employee_list:
            user = AttendanceUser(employee_data)
            if user.is_fired() and user.get_id() not in employee_ignore:
                collection.add(user)

    return collection


def load_attendance_time(collection: AttendanceCollection, date: datetime):
    for user in collection.get_collection().values():
        attendance_list = BosscontrolApi().get_employee_record_by_date(user.get_id(), date)
        attendance_list.sort()
        for timestamp in attendance_list:
            user.get_attendance().add(timestamp)
