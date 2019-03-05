from jira.api import JiraApi
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

    for issue in data.values():
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


def check_no_assignee(jql: str):
    collection = JiraApi().search(jql)
    Chat().post_message(channel='pmo_room_without_pmo', blocks=get_template(collection.get_collection()))
