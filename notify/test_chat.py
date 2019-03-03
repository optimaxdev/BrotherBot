from unittest import TestCase

from notify.chat import Chat


class TestChat(TestCase):
    def test_post_message(self):
        self.assertTrue(Chat().post_message("pmo_room_without_pmo", "test"))

    def test_me_message(self):
        self.assertTrue(Chat().me_message("pmo_room_without_pmo", "said TEST modofuka!!!"))
