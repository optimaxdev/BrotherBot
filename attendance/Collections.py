import datetime

from attendance.bosscontrol import AttendanceUser
from basic.Collection import Collection


class UserCollection(Collection):
    def add_user(self, user: AttendanceUser):
        self.add(user.get_id(), user)

    def get_absent_list(self, date: datetime) -> list:
        return [user for user in self.get_list() if user.get_attendance().is_absent(date)]

    def get_late_list(self, date: datetime, start_work_hour: int, reverse=True) -> list:
        user_is_late = []
        for user in self.get_list():
            attendance = user.get_attendance()
            if not attendance.is_absent(date) and (attendance.get_first(date).hour >= start_work_hour and attendance.get_first(date).minute > 0):
                user_is_late.append(user)
        return sorted(user_is_late, key=lambda k: k.get_attendance().get_first(date), reverse=reverse)
