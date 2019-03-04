import datetime
import click
from flask.cli import AppGroup

from app import app
from app.attendance.absent import notify_absent_employees
from app.attendance.late import notify_late_employees

employee_cli = AppGroup('employee')


@employee_cli.command()
@click.option('--date', default=datetime.datetime.now())
def notify_absent(date):
    notify_absent_employees(date)


@employee_cli.command()
@click.option('--date', default=datetime.datetime.now())
def notify_late(date):
    notify_late_employees(datetime.datetime.strptime(date, '%Y-%m-%d'))


app.cli.add_command(employee_cli)
