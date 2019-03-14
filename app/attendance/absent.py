import datetime
from pprint import pprint

from attendance.Collections import UserCollection
from notify.chat import Chat


def get_template_absent(data: list, date: datetime):
    fields = []
    for username in data:
        fields.append({"type": "mrkdwn", "text": "*" + username.name + "*"})
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


def notify_absent_employees(date: datetime, channel='general'):
    collection = UserCollection()
    Chat().post_message(blocks=get_template_absent(collection.get_absent_list(date), date), channel=channel)

