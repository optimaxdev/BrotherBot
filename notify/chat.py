import json
import requests
from config import Config


class Chat:
    def __init__(self):
        self.token = Config.CHAT_SLACK_TOKEN
        self.room = Config.CHAT_SLACK_ROOM

    def post_message(self, channel=None, message=None, blocks=None):
        params = {}
        if channel is None:
            params['channel'] = Config.CHAT_SLACK_ROOM
        if message is not None:
            params['text'] = message
        if blocks is not None:
            params['blocks'] = blocks

        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            json=params,
            headers={
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': 'Bearer %s' % self.token
            }
        )
        return json.loads(response.text)['ok'] is True
