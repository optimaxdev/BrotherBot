import json

import requests

from config import Config


DEFAULT_UVP_JQL = 'project = UVP AND status in ("In Progress", Testing, "Code Review", "Test Failed", ' \
                  '"Create Checklist", "Write Test Cases") AND assignee in (oldgraff, faceplay, Vladimir_Rydvan, ' \
                  'skazqa0702) '


class JiraStatus:
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data

    def get_id(self):
        return self.data['id']

    def get_name(self):
        return self.data['name']


class JiraUser:
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data

    def get_id(self):
        return self.data['key']

    def get_email(self):
        return self.data['emailAddress']

    def get_display_name(self):
        return self.data['displayName']


class JiraIssue:
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data
        self.assignee = None
        self.status = JiraStatus(data['fields']['status'])
        if data['fields']['assignee'] is not None:
            self.assignee = JiraUser(data['fields']['assignee'])

    def get_id(self):
        return self.data['id']

    def get_key(self):
        return self.data['key']

    def get_status(self):
        return self.status

    def get_assignee(self):
        return self.assignee


class JiraIssueCollection:
    def __init__(self, data=None) -> None:
        super().__init__()
        self.collection = {}
        if data is not None:
            self.add_from_list(data)

    def add_from_list(self, issue_list: list):
        for issue in issue_list:
            self.add(JiraIssue(issue))

    def add(self, issue: JiraIssue):
        self.collection[issue.get_id()] = issue
        return self

    def get_collection(self):
        return self.collection

    def get_length(self):
        return len(self.collection.items())


class JiraApi:

    def __init__(self) -> None:
        super().__init__()
        self.username = Config().JIRA_USERNAME
        self.password = Config().JIRA_PASSWORD
        self.host = "https://jira.gusadev.com/rest"

    def search(self, jql: str):
        response = requests.get(self.host + '/api/2/search', params={'jql': jql}, auth=(self.username, self.password))
        if not response.ok:
            return None
        return JiraIssueCollection(json.loads(response.text)['issues'])
