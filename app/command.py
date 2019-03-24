from datetime import datetime
import click
from flask.cli import AppGroup

from app import app
from app.attendance.absent import AbsentNotify
from app.attendance.late import LateNotify
from app.workflow.validation.duedate import DueDateOutdatedNotify
from app.workflow.validation.duedate_not_set import DueDateNotSetNotify
from app.workflow.validation.noassignee import NoAssigneeNotify
from app.workflow.validation.singlestatus import SingleStatusNotify
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
    notify = AbsentNotify(date=get_date(date))
    notify.report('slack', channel)


@employee_cli.command()
@click.option('--date', default=datetime.now().strftime('%Y-%m-%d'))
@click.option('--channel', default='general')
def notify_late(date, channel):
    notify = LateNotify(date=get_date(date))
    notify.report('slack', channel)


@workflow_cli.command()
@click.option('--channel', default=None)
def validate_single_status(channel):
    notify = SingleStatusNotify()
    for item in Config.VALIDATOR_SINGLE_STATUS:
        notify.jql = item['jql']
        notify.report('slack', item['channel'] if channel is None else channel)


@workflow_cli.command()
@click.option('--channel', default=None)
def validate_no_assignee(channel):
    notify = NoAssigneeNotify()
    for item in Config.VALIDATOR_NO_ASSIGNEE:
        notify.jql = item['jql']
        notify.report('slack', channel=item['channel'] if channel is None else channel)


@workflow_cli.command()
@click.option('--channel', default=None)
def validate_due_date(channel):
    notify_not_set = DueDateNotSetNotify()
    notify_due_date = DueDateOutdatedNotify()
    for item in Config.VALIDATOR_DUE_DATE:
        notify_not_set.jql = item['jql']
        notify_due_date.jql = item['jql']
        notify_not_set.report('slack', item['channel'] if channel is None else channel)
        notify_due_date.report('slack', item['channel'] if channel is None else channel)


app.cli.add_command(employee_cli)
app.cli.add_command(workflow_cli)
