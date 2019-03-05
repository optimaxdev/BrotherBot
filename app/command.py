import datetime
import click
from flask.cli import AppGroup

from app import app
from app.attendance.absent import notify_absent_employees
from app.attendance.late import notify_late_employees
from app.workflow.validation.noassignee import check_no_assignee
from app.workflow.validation.singlestatus import check_single_status

employee_cli = AppGroup('employee')
workflow_cli = AppGroup('workflow')


@employee_cli.command()
@click.option('--date', default=datetime.datetime.now())
def notify_absent(date):
    notify_absent_employees(date)


@employee_cli.command()
@click.option('--date', default=datetime.datetime.now().strftime('%Y-%m-%d'))
def notify_late(date):
    notify_late_employees(datetime.datetime.strptime(date, '%Y-%m-%d'))


@workflow_cli.command()
def validate_single_status():
    check_single_status('project in (GUSA, UVP, BAC, BUG, GRO, ANT, GD, OPT, OT) AND issuetype in (Bug, Improvement, '
                        '"New Feature", QA, Story, Task) AND status in ("In Progress", Testing, "Code Review", '
                        '"Create Checklist", "Write Test Cases")')


@workflow_cli.command()
def validate_no_assignee():
    check_no_assignee('status in ("In Progress", Testing, "Code Review", "In Development", "Create Checklist", '
                      '"Write Test Cases") AND assignee in (EMPTY) ')


app.cli.add_command(employee_cli)
app.cli.add_command(workflow_cli)
