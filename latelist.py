import datetime

import click
from app import app
from attendance.bosscontrol import BosscontrolApi
from notify.chat import Chat


@click.command()
def send_late_list():
    Chat().post_message("pmo_room_without_pmo", "Сейчас чо-как посчитаем ")
    users = BosscontrolApi().get_employee_records_by_date(datetime.datetime.now())

    user_absent = []
    user_in_office = []
    for user in users:
        if len(user['attendance_record']) is 0:
            user_absent.append(user['name'])
        else:
            user_in_office.append(user)
    message = "Сегодня отсутствуют следующие люди:\n" + "\n".join(user_absent)
    Chat().post_message("pmo_room_without_pmo", message)

    user_in_office_sorted = sorted(user_in_office, key=lambda k: k['attendance_record'][0], reverse=True)
    user_name_in_office = []
    for user in user_in_office_sorted:
        time_entrance = user['attendance_record'][0]
        if time_entrance.hour >= 10:
            user_name_in_office.append("%s - %s" % (time_entrance.strftime("%H:%M"), user['name']))
    message = "Рейтинг опоздунов \n" + "\n".join(user_name_in_office)
    Chat().post_message("pmo_room_without_pmo", message)


if __name__ == '__main__':
    send_late_list()
