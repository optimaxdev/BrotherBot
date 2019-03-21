from app.notify import NotifyMessage
from attendance.Collections import UserCollection


class AbsentNotify(NotifyMessage):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.date = kwargs['date']

    def _get_data(self):
        data = []
        for item in UserCollection().get_absent_list(self.date):
            data.append({
                'name': item.name
            })
        return data

    def _get_template(self, data):
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Cписок отсутствующих людей на *%s*\n"
                            "Если человек в офисе, то попросите его отметиться. Он явно забыл это сделать." % (self.date.strftime("%d.%m.%Y"))
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [{"type": "mrkdwn", "text": "*" + item['name'] + "*"} for item in data]
            }
        ]
