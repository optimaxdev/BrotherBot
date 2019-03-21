from datetime import datetime
from unittest import TestCase

from app.attendance.absent import AbsentNotify


class TestAbsentNotify(TestCase):
    def test__get_data(self):
        date = datetime.strptime('2019-03-21', '%Y-%m-%d')
        notify = AbsentNotify(date=date)
        self.assertEqual([
            {
                'text': {
                    'text': 'Cписок отсутствующих людей на *21.03.2019*\nЕсли человек в офисе, то попросите его '
                            'отметиться. Он явно забыл это сделать.',
                    'type': 'mrkdwn'
                },
                'type': 'section'
            },
            {
                'type': 'divider'
            },
            {
                'fields': [
                    {
                        'text': '*test_name*',
                        'type': 'mrkdwn'
                    }
                ],
                'type': 'section'
            }],
            notify._get_template([{'name': 'test_name'}])
        )
