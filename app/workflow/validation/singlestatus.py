from jira.Api import Api
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


def check_single_status(jql: str, channel='general'):
    collection = Api().search(jql)

    unique_index = {}
    for item in collection.get_list():
        if item.assignee is None:
            continue
        index = '_'.join([item.assignee.ident, item.status.ident])
        if unique_index.get(index) is None:
            unique_index[index] = [item]
        else:
            unique_index[index].append(item)

    validate_error = {key: val for key, val in unique_index.items() if len(val) > 1}
    if len(validate_error) > 0:
        Chat().post_message(blocks=get_template(validate_error), channel=channel)
