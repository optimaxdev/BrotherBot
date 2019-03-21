from unittest import TestCase
from unittest.mock import MagicMock

import requests

from config import Config
from notify.chat import SlackChat


class TestSlackChat(TestCase):
    def _create_mock_post(self, text: str):
        class ObjectForTest(object):
            pass

        response = ObjectForTest()
        response.text = text
        requests.post = MagicMock(return_value=response)

    def test_send_message(self):
        Config.CHAT_SLACK_TOKEN = 'token'

        self._create_mock_post('{"ok": true}')

        chat = SlackChat()
        self.assertEqual(True, chat.send_message('message1', 'channel1'))
        self.assertEqual({
                'json': {'channel': 'channel1', 'text': 'message1'},
                'headers': {'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer token'}
            },
            requests.post.call_args_list[0][1]
        )

    def test_send_blocks(self):
        Config.CHAT_SLACK_TOKEN = 'token'

        self._create_mock_post('{"ok": true}')

        chat = SlackChat()
        self.assertEqual(True, chat.send_message(['block1'], 'channel1'))
        self.assertEqual({
                'json': {'channel': 'channel1', 'blocks': ['block1']},
                'headers': {'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer token'}
            },
            requests.post.call_args_list[0][1]
        )

    def test_send_blocks_and_message(self):
        Config.CHAT_SLACK_TOKEN = 'token'

        self._create_mock_post('{"ok": true}')

        chat = SlackChat()
        self.assertEqual(True, chat.send_message('message1', 'channel1'))
        self.assertEqual({
                'json': {'channel': 'channel1', 'text': 'message1'},
                'headers': {'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer token'}
            },
            requests.post.call_args_list[0][1]
        )
