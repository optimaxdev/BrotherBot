import datetime
import json
import requests
from cachetools import TTLCache, cached

from config import Config

cache = TTLCache(maxsize=100, ttl=300)


class BosscontrolApi:
    """
    Documentation is here https://www.bosscontrol.ru/api/docs/
    """
    def __init__(self):
        self.username = Config().ATTENDANCE_BOSSCONTROL_USERNAME
        self.password = Config().ATTENDANCE_BOSSCONTROL_PASSWORD
        self.host = "https://www.bosscontrol.ru/timeattendance/json/"
        self.department_id = [
            "bosscontrol_internal_grp_15355",
            "bosscontrol_internal_grp_15359",
            "bosscontrol_internal_grp_15356",
            "bosscontrol_internal_grp_15357",
            "bosscontrol_internal_grp_15358"
        ]

    @cached(cache)
    def get_employee_list_by_department(self, department_id):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        response = requests.post(self.host, json={
            'id': 'request_id',
            'method': 'timeattendance.getDepartmentEmployeesForPeriod',
            'params': [self.username, self.password, department_id, current_date, current_date]
        })

        result = []
        for user in json.loads(response.text)['result']:
            if user['discharge_date'] is '':
                result.append(user)

        return result

    def get_employees_list(self) -> list:
        result = []
        for department_id in self.department_id:
            result.extend(self.get_employee_list_by_department(department_id))
        return result

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

    def get_employee_records_by_date(self, date: datetime) -> list:
        result = []
        for user in self.get_employees_list():
            user['attendance_record'] = self.get_employee_record_by_date(user['code'], date)
            user['attendance_record'].sort()
            result.append(user)
        return result

