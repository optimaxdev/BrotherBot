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
        self.update(kwargs)
        del kwargs
        self.update(locals())
        del self.self

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


class JiraIssue(Object):
    def __init__(self, host=Config.JIRA_HOST, **kwargs) -> None:
        super().__init__()
        self._host = None
        self._ident = None
        self._key = None
        self._issue_type = None
        self._summary = None
        self._due_date = None
        self._assignee = None
        self._project = None
        self._status = None
        self.update(kwargs)
        del kwargs
        self.update(locals())
        del self.self

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

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
        return '%s/browse/%s' % (self.host, self.key)

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
