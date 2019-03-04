import datetime

import click
from app import app
from attendance.bosscontrol import BosscontrolApi
from notify.chat import Chat


def get_template_absent(data: list):
    template = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Cписок отсутствующих сегодня людей.\nЕсли человек в офисе, то посоветуйте ему отметиться. Он явно забыл это сделать."
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": []
        }
    ]
    for username in data:
        template[2]['fields'].append({"type": "mrkdwn", "text": "*" + username + "*"})
    return template


@click.command()
def send_late_list():
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
