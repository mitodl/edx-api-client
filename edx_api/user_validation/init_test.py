"""
Test responses from user_validation api.
"""

import json
import os
from unittest import TestCase
from urllib.parse import urljoin

import requests_mock

from edx_api.client import EdxApi
from .models import UserValidationResult


class UserValidationTestCase(TestCase):
    """
    Tests for the UserValidation API client.
    """

    base_url = "https://edx.example.com"

    def setUp(self):
        super().setUp()

        with open(
            os.path.join(
                os.path.dirname(__file__),
                "fixtures/user_validation.json",
            )
        ) as file:  # pylint: disable=redefined-builtin
            self.validation_data = json.load(file)
        self.client = EdxApi({"access_token": ""}, self.base_url)

    def get_mock_response(self, key):
        """
        Return the validation_decisions response from the fixture.
        """
        return self.validation_data['validation_responses'].get(key, {})

    @requests_mock.Mocker()
    def test_validate_user_registration_info(self, mock_req):
        """
        Test that validate_user_registration_info validates name and username.
        """
        test_cases = [
            ('valid_name', {'name': ''}, {'name': 'test_name'}),
            ('invalid_name', {'name': 'Invalid name'}, {'name': 'http://test_name'}),
            ('valid_username', {'username': ''}, {'username': 'test_username'}),
            ('invalid_username', {'username': 'Invalid username'}, {'username': '!test_username'}),
        ]

        for key, expected_validation_decisions, request_data in test_cases:
            with self.subTest(key=key):
                mock_req.post(
                    urljoin(self.base_url, '/api/user/v1/validation/registration'),
                    json=self.get_mock_response(key)
                )
                validation_response = self.client.user_validation.validate_user_registration_info(request_data)
                self.assertIsInstance(validation_response, UserValidationResult)
                self.assertDictEqual(validation_response.validation_decisions, expected_validation_decisions)
