import datetime

from attendance.bosscontrol import load_employees, load_attendance_time
from notify.chat import Chat


def get_template(data: list, date: datetime):
    template = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Я нашел *%s* опоздавших на *%s*" % (len(data), date.strftime("%d.%m.%Y"))
            }
        }
    ]
    for user in data:
        template.append({"type": "divider"})
        template.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*%s*\nПришел в %s\nОпоздание: %s минут" % (
                        user.get_name(),
                        user.get_attendance().get_first(date).strftime("%H:%M"),
                        '1234'
                    )
                }
            }
        )
    return template


def notify_late_employees(date: datetime):
    collection = load_employees()
    load_attendance_time(collection, date)
    data = collection.get_late_rate_list(date)
    Chat().post_message(blocks=get_template(data, date))
