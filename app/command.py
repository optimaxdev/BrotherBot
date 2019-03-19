from datetime import datetime
import click
from flask.cli import AppGroup

from app import app
from app.attendance.absent import notify_absent_employees
from app.attendance.late import notify_late_employees
from app.workflow.validation.duedate import check_due_date
from app.workflow.validation.noassignee import check_no_assignee
from app.workflow.validation.singlestatus import check_single_status

employee_cli = AppGroup('employee')
workflow_cli = AppGroup('workflow')


def get_date(date):
    result = datetime.now()
    try:
        if type(date) == str:
            result = datetime.strptime(date, '%Y-%m-%d')
    except Exception:
        pass
    return result


@employee_cli.command()
@click.option('--date', default=datetime.now())
@click.option('--channel', default='general')
def notify_absent(date, channel):
    notify_absent_employees(get_date(date), channel=channel)


@employee_cli.command()
@click.option('--date', default=datetime.now().strftime('%Y-%m-%d'))
@click.option('--channel', default='general')
def notify_late(date, channel):
    notify_late_employees(get_date(date), channel)


@workflow_cli.command()
def validate_single_status():
    check_single_status('project in (UVP, BAC, BUG, GRO, ANT, GD, OPT, OT) AND issuetype in (Bug, Improvement, '
                        '"New Feature", QA, Story, Task) AND status in ("In Progress", Testing, "Code Review", '
                        '"Create Checklist", "Write Test Cases")', channel='general')
    check_single_status('project in (GUSA, Bugtracker) AND Sprint = "Rebels" AND  issuetype in (Bug, Improvement, '
                        '"New Feature", QA, Task) AND status in ("In Progress", Testing, "Code Review", '
                        '"Create Checklist", "Write Test Cases")', channel='rebels')
    check_single_status('project in (GUSA, Bugtracker) AND Sprint = "D.E.H.T.A." AND  issuetype in (Bug, Improvement, '
                        '"New Feature", QA, Task) AND status in ("In Progress", Testing, "Code Review", '
                        '"Create Checklist", "Write Test Cases")', channel='dehta')


@workflow_cli.command()
def validate_no_assignee():
    check_no_assignee('status in ("In Progress", Testing, "Code Review", "In Development", "Create Checklist", '
                      '"Write Test Cases") AND assignee in (EMPTY) ')


@workflow_cli.command()
def validate_due_date():
    check_due_date('project in (OT, UVP) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is '
                   'EMPTY )', 'ottica')
    check_due_date('project in (GRO, BUG) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is '
                   'EMPTY )', 'growth')
    check_due_date('project in (ANT) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases", "In Development") AND (due <= '
                   '"0" OR due is EMPTY )', 'analytics-team')
    check_due_date('project in (GD) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is '
                   'EMPTY )', 'devops')
    check_due_date('project in (BAC) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is '
                   'EMPTY )', 'backend_team')
    check_due_date('project in (GUSA, OPT) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is '
                   'EMPTY )', 'general')


app.cli.add_command(employee_cli)
app.cli.add_command(workflow_cli)
