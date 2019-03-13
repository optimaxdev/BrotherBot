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


def get_employee_list_by_department(department_id: str, date: datetime) -> list:
    selected_date = date.strftime("%Y-%m-%d")
    response = requests.post(__HOST__, json={
        'id': 'request_id',
        'method': 'timeattendance.getDepartmentEmployeesForPeriod',
        'params': [
            __USERNAME__,
            __PASSWORD__,
            department_id,
            selected_date,
            selected_date
        ]
    })

    result = []
    try:
        result = json.loads(response.text)['result']
    except Exception:
        pass
    return result


def get_employee_list() -> list:
    result = []
    for department_id in Config.ATTENDANCE_DEPARTMENT:
        employee_list = get_employee_list_by_department(department_id, datetime.now())
        for employee_data in employee_list:
            if 'code' not in employee_data.keys():
                continue
            if employee_data['code'] not in Config.ATTENDANCE_USER_IGNORE:
                result.append(employee_data)
    return result


def get_employee_record_by_date(employee_id: str, date: datetime) -> list:
    response = requests.post(__HOST__, json={
        'id': 'request_id',
        'method': 'timeattendance.getEmployeeRecords',
        'params': [
            __USERNAME__,
            __PASSWORD__,
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
