"""
Test responses from user_validation api.
"""

import pytest
from urllib.parse import urljoin

from edx_api.client import EdxApi
from .models import UserValidationResult


@pytest.mark.parametrize(
    "expected_validation_decisions, request_data, mock_response",
    [
        (
            {'name': ''},
            {'name': 'test_name'},
            {"validation_decisions": {"name": ""}}
        ),
        (
            {'name': 'Invalid name'},
            {'name': 'http://test_name'},
            {"validation_decisions": {"name": "Invalid name"}}
        ),
        (
            {'username': ''},
            {'username': 'test_username'},
            {"validation_decisions": {"username": ""}}
        ),
        (
            {'username': 'Invalid username'},
            {'username': '!test_username'},
            {"validation_decisions": {"username": "Invalid username"}}
        ),
    ]
)
def test_validate_user_registration_info(requests_mock, expected_validation_decisions, request_data, mock_response):
    """
    Test that validate_user_registration_info validates name and username.
    """
    base_url = "https://edx.example.com"
    client = EdxApi({"access_token": ""}, base_url)

    requests_mock.post(
        urljoin(base_url, '/api/user/v1/validation/registration'),
        json=mock_response
    )

    validation_response = client.user_validation.validate_user_registration_info(request_data)

    assert isinstance(validation_response, UserValidationResult)
    assert validation_response.validation_decisions == expected_validation_decisions
