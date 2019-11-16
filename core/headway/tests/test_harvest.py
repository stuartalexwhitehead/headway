from django.test import TestCase
from django.conf import settings
from requests.compat import urljoin
import requests_mock

from headway.harvest import get_user_by_email


@requests_mock.Mocker()
class GetUserByEmailTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.page1 = {
            "users": [{
                "id": 1,
                "first_name": "A",
                "last_name": "Bloggs",
                "email": "a@headway.com",
            }, {
                "id": 2,
                "first_name": "B",
                "last_name": "Bloggs",
                "email": "b@headway.com",
            }],
            "per_page": 2,
            "total_pages": 3,
            "total_entries": 6,
            "next_page": 2,
            "previous_page": None,
            "page": 1,
            "links": {
                "first": urljoin(settings.HARVEST_BASE_URL, '/v2/users', '?page=1'),
                "next": urljoin(settings.HARVEST_BASE_URL, '/v2/users', '?page=2'),
                "previous": None,
                "last": urljoin(settings.HARVEST_BASE_URL, '/v2/users', '?page=3')
            }
        }

        cls.page2 = {
            "users": [{
                "id": 3,
                "first_name": "C",
                "last_name": "Bloggs",
                "email": "c@headway.com",
            }, {
                "id": 4,
                "first_name": "D",
                "last_name": "Bloggs",
                "email": "d@headway.com",
            }],
            "per_page": 2,
            "total_pages": 3,
            "total_entries": 6,
            "next_page": 3,
            "previous_page": 1,
            "page": 2,
            "links": {
                "first": urljoin(settings.HARVEST_BASE_URL, '/v2/users', '?page=1'),
                "next": urljoin(settings.HARVEST_BASE_URL, '/v2/users', '?page=3'),
                "previous": urljoin(settings.HARVEST_BASE_URL, '/v2/users', '?page=1'),
                "last": urljoin(settings.HARVEST_BASE_URL, '/v2/users', '?page=3')
            }
        }

        cls.page3 = {
            "users": [{
                "id": 5,
                "first_name": "E",
                "last_name": "Bloggs",
                "email": "e@headway.com",
            }, {
                "id": 6,
                "first_name": "F",
                "last_name": "Bloggs",
                "email": "f@headway.com",
            }],
            "per_page": 2,
            "total_pages": 3,
            "total_entries": 6,
            "next_page": None,
            "previous_page": 2,
            "page": 3,
            "links": {
                "first": urljoin(settings.HARVEST_BASE_URL, '/v2/users', '?page=1'),
                "next": None,
                "previous": urljoin(settings.HARVEST_BASE_URL, '/v2/users', '?page=2'),
                "last": urljoin(settings.HARVEST_BASE_URL, '/v2/users', '?page=3')
            }
        }

    def test_exists_single_page(self, m):
        m.get(requests_mock.ANY, json=self.page1)
        res = get_user_by_email("b@headway.com")

        self.assertIsNotNone(res)
        self.assertEqual(res, self.page1["users"][1])

    def test_exists_multiple_page(self, m):
        m.get(requests_mock.ANY, [{"json": self.page1}, {"json": self.page2}, {"json": self.page3}])
        res = get_user_by_email("e@headway.com")

        self.assertIsNotNone(res)
        self.assertEqual(res, self.page3["users"][0])

    def test_not_exists_multiple_page(self, m):
        m.get(requests_mock.ANY, [{"json": self.page1}, {"json": self.page2}, {"json": self.page3}])
        res = get_user_by_email("x@headway.com")

        self.assertIsNone(res)

    def test_http_error(self, m):
        m.get(requests_mock.ANY, status_code=500)
        res = get_user_by_email("a@headway.com")

        self.assertIsNone(res)
