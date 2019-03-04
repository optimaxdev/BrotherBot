import json
import requests
from config import Config


class Chat:
    def __init__(self):
        self.token = Config.CHAT_SLACK_TOKEN
        self.room = Config.CHAT_SLACK_ROOM

    def post_message(self, channel=None, message=None, blocks=None):
        params = {
            'token': self.token,
        }
        if channel is None:
            params['channel'] = Config.CHAT_SLACK_ROOM
        if message is not None:
            params['text'] = message

        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            params=params,
            header={'Content-Type': 'application/json'},
            json=blocks
        )
        return json.loads(response.text)['ok'] is True
