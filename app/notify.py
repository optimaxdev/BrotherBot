from notify.chat import chat as chat_factory


class NotifyMessage(object):
    def _get_template(self, data):
        raise NotImplementedError()

    def _get_data(self):
        raise NotImplementedError()

    def report(self, chat, channel):
        data = self._get_data()
        if not data:
            return

        chat_factory(chat).send_message(self._get_template(data), channel)
