from unittest import TestCase

from notify.chat import chat, SlackChat


class TestChat(TestCase):
    def test_chat(self):
        self.assertEqual(SlackChat, type(chat('slack')))

    def test_chat_raise_error(self):
        with self.assertRaises(AssertionError):
            chat('wrong-chat')
