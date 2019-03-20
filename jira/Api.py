import json
from datetime import datetime

import requests

from config import Config
from jira.Collections import IssueCollection
from jira.Objects import IssueObject, StatusObject, ProjectObject, UserObject


class Api:
    def __init__(self) -> None:
        super().__init__()
        self.username = Config.JIRA_USERNAME
        self.password = Config.JIRA_PASSWORD
        self.host = Config.JIRA_HOST

    def _make_get(self, url: str, params) -> dict:
        response = requests.get(
            '%s%s' % (self.host, url),
            params=params,
            auth=(self.username, self.password)
        )
        if not response.ok:
            return {}

        data = {}
        try:
            data = json.loads(response.text)
        except Exception:
            pass

        return data

    def _create_datetime(self, date, format='%Y-%m-%d %H:%M:%S'):
        result = None
        try:
            result = datetime.strptime(date, format)
        except ValueError:
            if format != '%Y-%m-%d':
                result = self._create_datetime(date, '%Y-%m-%d')
        except TypeError:
            pass
        return result

    def _create_project(self, data: dict) -> ProjectObject:
        return ProjectObject(
            ident=data['id'],
            name=data['name']
        )

    def _create_status(self, data: dict) -> StatusObject:
        return StatusObject(
            ident=data['id'],
            name=data['name']
        )

    def _create_user(self, data) -> UserObject:
        user = UserObject()
        if data is None:
            return user
        user.ident = data['key']
        user.display_name = data['displayName']
        user.email = data['emailAddress']
        return user

    def search(self, jql: str) -> IssueCollection:
        collection = IssueCollection()

        issue_data_list = []
        try:
            issue_data_list = self._make_get('/rest/api/2/search', {'jql': jql, 'maxResults': 1000})['issues']
        except Exception:
            pass

        for item in issue_data_list:
            issue = IssueObject(
                ident=item['id'],
                key=item['key'],
                summary=item['fields']['summary'],
                type=item['fields']['issuetype']['name'],
                due_date=self._create_datetime(item['fields']['duedate']),
                assignee=self._create_user(item['fields']['assignee']),
                project=self._create_project(item['fields']['project']),
                status=self._create_status(item['fields']['status'])
            )
            collection.add(issue)

        return collection
