import json
from datetime import datetime
import requests

from config import Config

__HOST__ = Config.ATTENDANCE_BOSSCONTROL_HOST
__USERNAME__ = Config.ATTENDANCE_BOSSCONTROL_USERNAME
__PASSWORD__ = Config.ATTENDANCE_BOSSCONTROL_PASSWORD

"""
    Documentation is here https://www.bosscontrol.ru/api/docs/
"""


class Api(object):
    def __init__(self) -> None:
        super().__init__()
        self.host = Config.ATTENDANCE_BOSSCONTROL_HOST
        self.username = Config.ATTENDANCE_BOSSCONTROL_USERNAME
        self.password = Config.ATTENDANCE_BOSSCONTROL_PASSWORD
        self.department_list = Config.ATTENDANCE_DEPARTMENT
        self.employee_ignore_list = Config.ATTENDANCE_USER_IGNORE

    def get_employee_list_by_department(self, department_id: str, date_start: datetime, date_end: datetime) -> list:
        response = requests.post(self.host, json={
            'id': 'request_id',
            'method': 'timeattendance.getDepartmentEmployeesForPeriod',
            'params': [
                self.username,
                self.password,
                department_id,
                date_start.strftime("%Y-%m-%d"),
                date_end.strftime("%Y-%m-%d")
            ]
        })

        result = []
        try:
            result = json.loads(response.text)['result']
        except Exception:
            pass
        return result

    def get_employee_list(self) -> list:
        result = []
        current_date = datetime.now()
        for department_id in self.department_list:
            employee_list = self.get_employee_list_by_department(department_id, current_date, current_date)
            for employee_data in employee_list:
                if 'code' not in employee_data.keys():
                    continue
                if employee_data['code'] not in self.employee_ignore_list:
                    result.append(employee_data)
        return result

    def get_employee_record_by_date(self, employee_id: str, date: datetime) -> list:
        response = requests.post(self.host, json={
            'id': 'request_id',
            'method': 'timeattendance.getEmployeeRecords',
            'params': [
                self.username,
                self.password,
                employee_id,
                date.strftime("%Y-%m-%d")
            ]
        })

        time_data = []
        try:
            time_data = json.loads(response.text)['result']
        except Exception:
            pass

        result = []
        for time in time_data:
            if 'timestamp' not in time.keys():
                continue
            result.append(datetime.strptime(time['timestamp'], '%Y-%m-%d %H:%M:%S'))
        return result
