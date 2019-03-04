import datetime

from attendance.bosscontrol import BosscontrolApi




class Attendance:
    def get_list_sorted_by_late(self, date: datetime):
        users = BosscontrolApi().get_employee_records_by_date(date)

