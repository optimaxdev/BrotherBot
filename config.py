import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    CHAT_SLACK_TOKEN = os.environ.get('CHAT_SLACK_TOKEN') or 'slack-token'

    ATTENDANCE_BOSSCONTROL_USERNAME = os.environ.get('ATTENDANCE_BOSSCONTROL_USERNAME') or 'bosscontrol-username'
    ATTENDANCE_BOSSCONTROL_PASSWORD = os.environ.get('ATTENDANCE_BOSSCONTROL_PASSWORD') or 'bosscontrol-password'