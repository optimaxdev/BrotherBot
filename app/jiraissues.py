from jira.api import JiraApi, DEFAULT_UVP_JQL
from notify.chat import Chat


def send_message(message):
    Chat().post_message('pmo_room_without_pmo', message)


def check_issue_unique():
    collection = JiraApi().search(DEFAULT_UVP_JQL)
    if collection is None:
        return
    if collection.get_length() is 0:
        send_message("Чтото ничего не нашел я по запросу и это уже зашквар. Проверь сам:\n%s" % DEFAULT_UVP_JQL)

    unique_index = {}
    for item_id, item in collection.get_collection().items():
        index = '_'.join([item.get_assignee().get_id(), item.get_status().get_id()])
        if unique_index.get(index) is None:
            unique_index[index] = [item]
        else:
            unique_index[index].append(item)

    for item_id, item in unique_index.items():
        if len(item) > 1:
            message = 'Найдено нарушение на борде по правилу 1 задача на 1 человека в определенном статусе'
            for issue in item:
                message = message + '\n%s статус %s, исполнитель %s' % (
                    issue.get_key(),
                    issue.get_status().get_name(),
                    issue.get_assignee().get_display_name()
                )
            send_message(message)
