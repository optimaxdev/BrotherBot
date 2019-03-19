from basic.Object import Object
from config import Config


class JiraProject(Object):
    def __init__(self, data=None) -> None:
        super().__init__()
        self.data = data

    def get_name(self) -> str:
        return self.data['name']


class JiraStatus(Object):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data

    def get_id(self):
        return self.data['id']

    def get_name(self) -> str:
        return self.data['name']


class JiraUser(Object):
    def __init__(self, **kwargs) -> None:
        super(JiraUser).__init__(**kwargs)
        self._email = None
        self._display_name = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        self._display_name = value


class IssueObject(Object):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._key = kwargs['key']
        self._issue_type = kwargs['issue_type']
        self._summary = kwargs['summary']
        self._due_date = kwargs['due_date'] if 'due_date' in kwargs else None
        self._assignee = kwargs['assignee'] if 'assignee' in kwargs else None
        self._project = kwargs['project']
        self._status = kwargs['status']

    @property
    def ident(self):
        return self._ident

    @ident.setter
    def ident(self, value):
        self._ident = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def assignee(self):
        return self._assignee

    @assignee.setter
    def assignee(self, value):
        self._assignee = value

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, project):
        self._project = project

    @property
    def url(self):
        return '%s/browse/%s' % (Config.JIRA_HOST, self.key)

    @property
    def type(self):
        return self._issue_type

    @type.setter
    def type(self, value):
        self._issue_type = value

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        self._due_date = value
