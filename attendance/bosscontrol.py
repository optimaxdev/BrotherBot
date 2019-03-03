# https://www.bosscontrol.ru/api/docs/


class BosscontrolApi:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.host = "https://www.bosscontrol.ru/timeattendance/json/"
        self.department_id = ""

    def get_employees_list(self) -> list:
        pass

    def get_employee_record_by_date(self, employee_id: str, date: str) -> list:
        pass
