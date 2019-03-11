from basic.Collection import Collection
from jira.api import JiraIssue


class IssueCollection(Collection):
    def add_issue(self, issue: JiraIssue):
        self.add(issue.get_id(), issue)
