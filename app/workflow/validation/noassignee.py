from jira.Api import Api
from notify.chat import Chat


def get_template(data):
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

    for issue in data.get_list():
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


def check_no_assignee(jql: str, channel='leads'):
    collection = Api().search(jql)
    if collection.get_length() == 0:
        return
    Chat().post_message(
        channel=channel,
        blocks=get_template(collection)
    )
