from app.notify import NotifyMessage
from jira.Api import Api


class NoAssigneeNotify(NotifyMessage):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.jql = kwargs['jql'] if 'jql' in kwargs else None

    @property
    def jql(self):
        return self._jql

    @jql.setter
    def jql(self, value):
        self._jql = value

    def _get_data(self):
        return Api().search(self.jql).get_list()

    def _get_template(self, data):
        template = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Нарушен принцип workflow: *задача в разработке должна иметь назначенного assignee*"
                }
            },
            {
                "type": "divider"
            }
        ]

        for issue in data:
            text = "• *<%s|%s>* %s | %s in _%s_" % (
                issue.url,
                issue.key,
                issue.summary,
                issue.type,
                issue.status.name
            )
            template.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            })
        return template
