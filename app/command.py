from datetime import datetime
import click
from flask.cli import AppGroup

from app import app
from app.attendance.absent import notify_absent_employees
from app.attendance.late import notify_late_employees
from app.workflow.validation.duedate import check_due_date
from app.workflow.validation.noassignee import check_no_assignee
from app.workflow.validation.singlestatus import check_single_status
from config import Config

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
@click.option('--channel', default=None)
def validate_single_status(channel):
    for item in Config.VALIDATOR_SINGLE_STATUS:
        check_single_status(item['jql'], channel=item['channel'] if channel is None else channel)


@workflow_cli.command()
@click.option('--channel', default=None)
def validate_no_assignee(channel):
    for item in Config.VALIDATOR_NO_ASSIGNEE:
        check_no_assignee(item['jql'], channel=item['channel'] if channel is None else channel)


@workflow_cli.command()
@click.option('--channel', default='leads')
def validate_due_date():
    check_due_date('project in (OT, UVP) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is '
                   'EMPTY )', 'ottica', channel=channel)
    check_due_date('project in (GRO, BUG) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is '
                   'EMPTY )', 'growth', channel=channel)
    check_due_date('project in (ANT) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases", "In Development") AND (due <= '
                   '"0" OR due is EMPTY )', 'analytics-team')
    check_due_date('project in (GD) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is '
                   'EMPTY )', 'devops', channel=channel)
    check_due_date('project in (BAC) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is '
                   'EMPTY )', 'backend_team')
    check_due_date('project in (GUSA, OPT) AND status in ("In Progress", '
                   'Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is '
                   'EMPTY )', 'general', channel=channel)


app.cli.add_command(employee_cli)
app.cli.add_command(workflow_cli)
