from unittest import TestCase

from app.notify import NotifyMessage


class TestNotifyMessage(TestCase):
    def test_raise_not_implemented(self):
        item = NotifyMessage()
        with self.assertRaises(NotImplementedError):
            item._get_template([])
        with self.assertRaises(NotImplementedError):
            item._get_data()
