import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    CHAT_SLACK_TOKEN = os.environ.get('CHAT_SLACK_TOKEN') or 'slack-token'
    CHAT_SLACK_ROOM = os.environ.get('CHAT_SLACK_ROOM') or 'pmo_room_without_pmo'

    ATTENDANCE_BOSSCONTROL_HOST = "https://www.bosscontrol.ru/timeattendance/json/"
    ATTENDANCE_BOSSCONTROL_USERNAME = os.environ.get('ATTENDANCE_BOSSCONTROL_USERNAME') or 'bosscontrol-username'
    ATTENDANCE_BOSSCONTROL_PASSWORD = os.environ.get('ATTENDANCE_BOSSCONTROL_PASSWORD') or 'bosscontrol-password'
    ATTENDANCE_DEPARTMENT = [
        "bosscontrol_internal_grp_15355",
        "bosscontrol_internal_grp_15359",
        "bosscontrol_internal_grp_15356",
        "bosscontrol_internal_grp_15357",
        "bosscontrol_internal_grp_15358"
    ]
    ATTENDANCE_USER_IGNORE = [
        'bosscontrol_internal_801591',
        'bosscontrol_internal_765085'
    ]
    ATTENDANCE_WORKING_HOUR_START = 10
    ATTENDANCE_WORKING_HOUR_FINISH = 19

    JIRA_HOST = os.environ.get('JIRA_HOST') or 'http://127.0.0.1'
    JIRA_USERNAME = os.environ.get('JIRA_USERNAME') or 'jira-username'
    JIRA_PASSWORD = os.environ.get('JIRA_PASSWORD') or 'jira-password'

    VALIDATOR_NO_ASSIGNEE = [
        {
            'channel': 'leads',
            'jql': 'status in ("In Progress", Testing, "Code Review", "In Development", "Create Checklist", '
                   '"Write Test Cases") AND assignee in (EMPTY) '
        }
    ]

    VALIDATOR_SINGLE_STATUS = [
        {
            'channel': 'leads',
            'jql': 'project in (BAC, GUSA, GRO, SUP, OPT, ANT, BUG, GD, WIN, OT, UVP) AND issuetype in (Bug, Improvement, '
                   '"New Feature", QA, Story, Task) AND status in ("In Progress", Testing, "Code Review", '
                   '"Create Checklist", "Write Test Cases")'
        },
        {
            'channel': 'leads',
            'jql': 'project = WIN AND status in ("In Progress")'
        },
        {
            'channel': 'rebels',
            'jql': 'project in (GUSA, BUG) AND Sprint = "Rebels" AND  issuetype in (Bug, Improvement, '
                   '"New Feature", QA, Task) AND status in ("In Progress", Testing, "Code Review", '
                   '"Create Checklist", "Write Test Cases")'
        },
        {
            'channel': 'dehta',
            'jql': 'project in (GUSA, BUG) AND Sprint = "D.E.H.T.A." AND  issuetype in (Bug, Improvement, '
                   '"New Feature", QA, Task) AND status in ("In Progress", Testing, "Code Review", '
                   '"Create Checklist", "Write Test Cases")'
        },
        {
            'channel': 'backend_team',
            'jql': 'project in (BAC, BUG) AND issuetype in (Bug, Improvement, "New Feature", QA, Task) AND status in ("In '
                   'Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases") '
        },
        {
            'channel': 'ottica',
            'jql': 'project in (UVP, OT, BUG) AND issuetype in (Bug, Improvement, "New Feature", QA, Task) AND status in ("In '
                   'Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases") '
        },
        {
            'channel': 'devops',
            'jql': 'project in (GD, SUP) AND issuetype in (Bug, Improvement, "New Feature", QA, Story, Task) AND status in ('
                   '"In Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases") '
        },
        {
            'channel': 'analytics-team',
            'jql': 'project in (ANT, BUG) AND issuetype in (Bug, Improvement, "New Feature", QA, Task) AND status in ("In '
                   'Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases") '
        },
        {
            'channel': 'growth',
            'jql': 'project in (GRO, BUG) AND issuetype in (Bug, Improvement, "New Feature", QA, Task) AND status in ("In '
                   'Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases") '
        }
    ]

    VALIDATOR_DUE_DATE = [
        {
            'channel': 'general',
            'jql': 'project in (GUSA, OPT) AND status in ("In Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is EMPTY)'
        },
        {
            'channel': 'backend_team',
            'jql': 'project in (BAC) AND status in ("In Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is EMPTY)'
        },
        {
            'channel': 'devops',
            'jql': 'project in (GD) AND status in ("In Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is EMPTY)'
        },
        {
            'channel': 'analytics-team',
            'jql': 'project in (ANT) AND status in ("In Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases", "In Development") AND (due <= "0" OR due is EMPTY)'
        }
        ,
        {
            'channel': 'growth',
            'jql': 'project in (GRO, BUG) AND status in ("In Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is EMPTY)'
        }
        ,
        {
            'channel': 'ottica',
            'jql': 'project in (OT, UVP) AND status in ("In Progress", Testing, "Code Review", "Create Checklist", "Write Test Cases") AND (due <= "0" OR due is EMPTY)'
        }
    ]
