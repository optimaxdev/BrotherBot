from app.notify import NotifyMessage
from attendance.Collections import UserCollection
from config import Config


class LateNotify(NotifyMessage):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.date = kwargs['date']

    def _get_data(self):
        data = []
        for item in UserCollection().get_late_list(self.date, Config.ATTENDANCE_WORKING_HOUR_START, True):
            data.append({
                'name': item.name,
                'time': item.time.get_first(self.date).strftime("%H:%M")
            })
            if len(data) >= 10:
                break
        return data

    def _get_template(self, data):
        template = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Топ *%s* опоздавших на *%s*:" % (len(data), self.date.strftime("%d.%m.%Y"))
                }
            }
        ]
        for item in data:
            template.append({"type": "divider"})
            template.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*%s* отметился в %s" % (item['name'], item['time'])
                    }
                }
            )
        return template
