from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

import httpretty as httpretty

from jira.Api import Api


class TestApi(TestCase):
    def test__create_datetime(self):
        self.assertEqual(datetime(2019, 1, 1, 1, 1, 1), Api()._create_datetime('2019-01-01 01:01:01'))
        self.assertEqual(datetime(2019, 1, 1, 0, 0, 0), Api()._create_datetime('2019-01-01'))
        self.assertEqual(None, Api()._create_datetime(1))

    def test__create_project(self):
        item = Api()._create_project({
            'id': 'id1',
            'name': 'name1'
        })
        self.assertEqual('id1', item.ident)
        self.assertEqual('name1', item.name)

    def test__create_status(self):
        item = Api()._create_status({
            'id': 'id1',
            'name': 'name1'
        })
        self.assertEqual('id1', item.ident)
        self.assertEqual('name1', item.name)

    def test__create_user(self):
        item = Api()._create_user({
            'key': 'id1',
            'displayName': 'name1',
            'emailAddress': 'email1'
        })
        self.assertEqual('id1', item.ident)
        self.assertEqual('name1', item.display_name)
        self.assertEqual('email1', item.email)

    def test__create_user_with_none_data(self):
        item = Api()._create_user(None)
        self.assertEqual(None, item.ident)
        self.assertEqual(None, item.display_name)
        self.assertEqual(None, item.email)

    @httpretty.activate
    def test__make_get(self):
        httpretty.register_uri(httpretty.GET, 'https://jira.gusadev.com/bad-json', body="Bad json string")
        httpretty.register_uri(httpretty.GET, 'https://jira.gusadev.com/error', body="Bad json string", status=500)
        httpretty.register_uri(httpretty.GET, 'https://jira.gusadev.com/data', body="[1, 2, {\"a\": 1}]")
        self.assertEqual({}, Api()._make_get('/bad-json', {}))
        self.assertEqual({}, Api()._make_get('/error', {}))
        self.assertEqual([1, 2, {'a': 1}], Api()._make_get('/data', {}))

    def test_search_false_data(self):
        api = Api()
        api._make_get = MagicMock(
            return_value="false-data"
        )
        self.assertEqual({}, api.search('project=key'))

    def test_search(self):
        api = Api()
        api._make_get = MagicMock(
            return_value={
                'issues': [
                    {
                        'id': 'id1',
                        'key': 'key1',
                        'fields': {
                            'duedate': '2019-01-01',
                            'summary': 'summary1',
                            'key': 'key1',
                            'assignee': None,
                            'project': {
                                'id': 'id1',
                                'name': 'name1'
                            },
                            'status': {
                                'id': 'id1',
                                'name': 'name1'
                            },
                            'issuetype': {
                                'name': 'name1'
                            }
                        }
                    }
                ]
            }
        )
        self.assertEqual(1, api.search('project=key').get_length())
