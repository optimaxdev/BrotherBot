import datetime

from attendance.bosscontrol import load_employees, load_attendance_time
from notify.chat import Chat


def get_template_absent(data: list, date: datetime):
    fields = []
    for username in data:
        fields.append({"type": "mrkdwn", "text": "*" + username.get_name() + "*"})
    date_string = date.strftime("%d.%m.%Y")
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Cписок отсутствующих людей на *%s*\n"
                        "Если человек в офисе, то посоветуйте ему отметиться. Он явно забыл это сделать." % date_string
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": fields
        }
    ]


def notify_absent_employees(date: datetime):
    collection = load_employees()
    load_attendance_time(collection, date)
    Chat().post_message(blocks=get_template_absent(collection.get_absent_employees(), date))

