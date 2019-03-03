import json
import requests
from config import Config


class Chat:
    def __init__(self):
        self.token = Config.CHAT_SLACK_TOKEN

    def post_message(self, channel: str, message: str):
        response = requests.post("https://slack.com/api/chat.postMessage", params={
            'token': self.token,
            'channel': channel,
            'text': message
        })
        return json.loads(response.text)['ok'] is True

    def me_message(self, channel: str, message: str):
        response = requests.post("https://slack.com/api/chat.meMessage", params={
            'token': self.token,
            'channel': channel,
            'text': message
        })
        return json.loads(response.text)['ok'] is True
