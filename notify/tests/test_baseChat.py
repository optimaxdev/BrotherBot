from unittest import TestCase

from notify.chat import BaseChat


class TestBaseChat(TestCase):
    def test_token(self):
        base = BaseChat()
        base.token = '1'
        self.assertEqual('1', base.token)

    def test_send_message(self):
        base = BaseChat()
        with self.assertRaises(NotImplementedError):
            base.send_message('message', ' channel')
