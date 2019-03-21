import json
import requests
from config import Config


class BaseChat(object):
    def __init__(self) -> None:
        super().__init__()
        self.token = None

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    def send_message(self, message, channel):
        raise NotImplementedError()


class SlackChat(BaseChat):
    def __init__(self):
        super().__init__()
        self.token = Config.CHAT_SLACK_TOKEN

    def send_message(self, message, channel):
        params = {
            'channel': channel
        }
        if type(message) == str:
            params['text'] = message
        else:
            params['blocks'] = message

        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            json=params,
            headers={
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': 'Bearer %s' % self.token
            }
        )

        return json.loads(response.text)['ok'] is True


def chat(type: str) -> BaseChat:
    if type == "slack": return SlackChat()
    raise AssertionError("Bad chat creation: " + type)
