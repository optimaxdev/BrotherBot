from datetime import datetime

from jira.Api import Api
from notify.chat import Chat


def get_template(data, title: str):
    template = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Нарушен принцип workflow: *%s*" % title
            }
        }
    ]

    for issue_list in data.values():
        user_name = issue_list[0].assignee.display_name
        template.append({"type": "divider"})
        template.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*%s*" % user_name
            }
        })
        for issue in issue_list:
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


# TODO: SHOULD check also for comments. I didnt implemented it. Need to find the way how to detect if comment is written
def check_due_date(jql: str, channel='general'):
    collection = Api().search(jql)

    error_empty_date = {}
    error_date_outdated = {}

    for issue in collection.get_list():
        if issue.assignee is None:
            continue
        user_id = issue.assignee.ident
        if issue.due_date is None:
            if not error_empty_date.get(user_id):
                error_empty_date[user_id] = []
            error_empty_date[user_id].append(issue)
            continue
        if issue.due_date.date() <= datetime.now().date():
            if not error_date_outdated.get(user_id):
                error_date_outdated[user_id] = []
            error_date_outdated[user_id].append(issue)

    if error_empty_date:
        Chat().post_message(blocks=get_template(error_empty_date, 'Due Date не установлен'), channel=channel)
    if error_date_outdated:
        Chat().post_message(blocks=get_template(error_date_outdated, 'Due Date устарел'), channel=channel)
