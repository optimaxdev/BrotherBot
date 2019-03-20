from basic.Object import Object
from config import Config


class ProjectObject(Object):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = kwargs['name']

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class StatusObject(Object):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = kwargs['name']

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class UserObject(Object):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.email = kwargs['email'] if 'email' in kwargs else None
        self.display_name = kwargs['display_name'] if 'display_name' in kwargs else None

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
        self.key = kwargs['key']
        self.type = kwargs['type']
        self.summary = kwargs['summary']
        self.due_date = kwargs['due_date'] if 'due_date' in kwargs else None
        self.assignee = kwargs['assignee'] if 'assignee' in kwargs else None
        self.project = kwargs['project']
        self.status = kwargs['status']
        self.host = kwargs['host'] if 'host' in kwargs else Config.JIRA_HOST

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

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
