import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    CHAT_SLACK_TOKEN = os.environ.get('CHAT_SLACK_TOKEN') or 'slack-token'
    CHAT_SLACK_ROOM = os.environ.get('CHAT_SLACK_ROOM') or 'pmo_room_without_pmo'

    ATTENDANCE_BOSSCONTROL_USERNAME = os.environ.get('ATTENDANCE_BOSSCONTROL_USERNAME') or 'bosscontrol-username'
    ATTENDANCE_BOSSCONTROL_PASSWORD = os.environ.get('ATTENDANCE_BOSSCONTROL_PASSWORD') or 'bosscontrol-password'

    JIRA_USERNAME = os.environ.get('JIRA_USERNAME') or 'jira-username'
    JIRA_PASSWORD = os.environ.get('JIRA_PASSWORD') or 'jira-password'
