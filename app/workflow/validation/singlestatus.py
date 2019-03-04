from jira.api import JiraApi, JiraIssue
from notify.chat import Chat


def get_template(data):
    template = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Нарушен принцип workflow: *в работе только одна задача на разработчика*"
            }
        }
    ]

    for issue_list in data.values():
        template.append({"type": "divider"})
        text = "*%s*\n\n" % issue_list[0].get_assignee().get_display_name()
        for issue in issue_list:
            text += "• *<%s|%s>* %s in _%s_\n" % (
                issue.get_url(), issue.get_key(),
                issue.get_type(), issue.get_status().get_name()
            )
        template.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        })
    return template


def check_single_status(jql: str):
    collection = JiraApi().search(jql)

    unique_index = {}
    for item_id, item in collection.get_collection().items():
        if item.get_assignee() is None:
            continue
        index = '_'.join([item.get_assignee().get_id(), item.get_status().get_id()])
        if unique_index.get(index) is None:
            unique_index[index] = [item]
        else:
            unique_index[index].append(item)

    validate_error = {key: val for key, val in unique_index.items() if len(val) > 1}
    if len(validate_error) > 0:
        Chat().post_message(blocks=get_template(validate_error))
