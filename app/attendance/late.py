from datetime import datetime

from attendance.Collections import UserCollection
from config import Config
from notify.chat import Chat


def get_template(data: list, date: datetime):
    template = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Я нашел *%s* опоздавших на *%s*\nТоп 10 опоздавших:" % (len(data), date.strftime("%d.%m.%Y"))
            }
        }
    ]
    counter = 0
    for user in data:
        template.append({"type": "divider"})
        template.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*%s* появился в %s" % (
                        user.name,
                        user.time.get_first(date).strftime("%H:%M")
                    )
                }
            }
        )
        counter += 1
        if counter >= 10:
            break

    return template


def notify_late_employees(date: datetime, channel: str):
    collection = UserCollection()
    Chat().post_message(
        blocks=get_template(collection.get_late_list(date, Config.ATTENDANCE_WORKING_HOUR_START, True), date),
        channel=channel
    )
