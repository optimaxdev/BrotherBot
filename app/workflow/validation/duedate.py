from datetime import datetime

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
        user_name = issue_list[0].get_assignee().get_display_name()
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
                issue.get_url(),
                issue.get_key(),
                issue.get_summary(),
                issue.get_type(),
                issue.get_status().get_name()
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
    collection = JiraApi().search(jql)

    error_empty_date = {}
    error_date_outdated = {}

    for issue in collection.get_collection().values():
        if issue.get_assignee() is None:
            continue
        user_id = issue.get_assignee().get_id()
        if issue.get_due_date() is None:
            if not error_empty_date.get(user_id):
                error_empty_date[user_id] = []
            error_empty_date[user_id].append(issue)
            continue
        if datetime.strptime(issue.get_due_date(), '%Y-%m-%d').date() <= datetime.now().date():
            if not error_date_outdated.get(user_id):
                error_date_outdated[user_id] = []
            error_date_outdated[user_id].append(issue)

    if error_empty_date:
        Chat().post_message(blocks=get_template(error_empty_date, 'Due Date не установлен'), channel=channel)
    if error_date_outdated:
        Chat().post_message(blocks=get_template(error_date_outdated, 'Due Date устарел'), channel=channel)
