from app.notify import NotifyMessage
from jira.Api import Api


class DueDateNotSetNotify(NotifyMessage):
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
        collection = Api().search(self.jql)

        error_empty_date = {}

        for issue in collection.get_list():
            if issue.assignee is None or issue.due_date is not None:
                continue
            user_id = issue.assignee.ident
            if not error_empty_date.get(user_id):
                error_empty_date[user_id] = []
            error_empty_date[user_id].append(issue)

        return error_empty_date.values()

    def _get_template(self, data):
        template = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Нарушен принцип workflow: *Due дата не установленна*"
                }
            }
        ]

        for issue_list in data:
            template.append({"type": "divider"})
            text = "*%s*\n\n" % issue_list[0].assignee.display_name
            for issue in issue_list:
                text += "• *<%s|%s>* %s in _%s_\n" % (
                    issue.url, issue.key,
                    issue.type, issue.status.name
                )
            template.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            })
        return template
