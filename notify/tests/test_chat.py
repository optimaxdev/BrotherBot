from unittest import TestCase
from unittest.mock import MagicMock

import requests

from config import Config
from notify.chat import Chat


class TestChat(TestCase):
    def _create_mock_post(self, text: str):
        class ObjectForTest(object):
            pass

        response = ObjectForTest()
        response.text = text
        requests.post = MagicMock(return_value=response)

    def test_post_message(self):
        Config.CHAT_SLACK_TOKEN = 'token'
        Config.CHAT_SLACK_ROOM = 'room'

        self._create_mock_post('{"ok": true}')

        chat = Chat()
        self.assertEqual(True, chat.post_message(message='test1', channel='channel1'))
        self.assertEqual({
                'json': {'channel': 'channel1', 'text': 'test1'},
                'headers': {'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer token'}
            },
            requests.post.call_args_list[0][1]
        )

    def test_post_blocks(self):
        Config.CHAT_SLACK_TOKEN = 'token'
        Config.CHAT_SLACK_ROOM = 'room'

        self._create_mock_post('{"ok": true}')

        chat = Chat()
        self.assertEqual(True, chat.post_message(blocks='test1', channel='channel1'))
        self.assertEqual({
                'json': {'channel': 'channel1', 'blocks': 'test1'},
                'headers': {'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer token'}
            },
            requests.post.call_args_list[0][1]
        )

    def test_post_blocks_and_message(self):
        Config.CHAT_SLACK_TOKEN = 'token'
        Config.CHAT_SLACK_ROOM = 'room'

        self._create_mock_post('{"ok": true}')

        chat = Chat()
        self.assertEqual(True, chat.post_message(blocks='test1', message='message1', channel='channel1'))
        self.assertEqual({
                'json': {'channel': 'channel1', 'text': 'message1'},
                'headers': {'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer token'}
            },
            requests.post.call_args_list[0][1]
        )
