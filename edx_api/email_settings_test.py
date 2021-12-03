"""test for change email settings"""
import requests_mock
from unittest import TestCase
from urllib.parse import urljoin

from edx_api.client import EdxApi
from edx_api.email_settings import EmailSettings


class TestEmailSettings(TestCase):

    @classmethod
    def setUpClass(cls):
        edx_base_url = "http://edx.example.com"
        cls.api_url = urljoin(edx_base_url, EmailSettings.api_url)
        cls.client = EdxApi({"access_token": "foobar"}, cls.api_url)
        cls.email_settings = cls.client.email_settings
        cls.json = {"success": "true"}
        cls.course_id = "course_id"

    @requests_mock.mock()
    def test_course_emails_subscription(self, mocked_request):
        mocked_request.post(self.api_url, json=self.json)
        response = self.email_settings.subscribe(self.course_id)
        self.assertDictEqual(
            mocked_request.last_request.json(),
            {"course_id": self.course_id, "receive_emails": "on"}
        )
        self.assertTrue(response)

    @requests_mock.mock()
    def test_course_emails_unsubscription(self, mocked_request):
        mocked_request.post(self.api_url, json=self.json)
        response = self.email_settings.unsubscribe(self.course_id)
        self.assertDictEqual(
            mocked_request.last_request.json(), {"course_id": self.course_id}
        )
        self.assertTrue(response)
