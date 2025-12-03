"""Tests for LTI Tools API client"""

from unittest.mock import Mock
from urllib.parse import urljoin

from edx_api.lti_tools import LTITools


class TestLTITools:
    """Tests for LTITools class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.requester = Mock()
        self.base_url = "https://example.edx.org"
        self.client = LTITools(self.requester, self.base_url)

    def test_init(self):
        """Test LTITools initialization"""
        assert self.client.requester == self.requester
        assert self.client.base_url == self.base_url

    def test_fix_lti_user_success(self):
        """Test fix_lti_user with successful response"""
        email = "test@example.com"
        expected_response = Mock()
        self.requester.post.return_value = expected_response

        result = self.client.fix_lti_user(email)

        self.requester.post.assert_called_once_with(
            urljoin(self.base_url, '/api/lti-user-fix/'),
            json={"email": email}
        )
        assert result == expected_response

    def test_fix_lti_user_with_different_credentials(self):
        """Test fix_lti_user with email"""
        email = "another@example.com"
        expected_response = Mock()
        self.requester.post.return_value = expected_response

        result = self.client.fix_lti_user(email)

        self.requester.post.assert_called_once_with(
            urljoin(self.base_url, '/api/lti-user-fix/'),
            json={"email": email}
        )
        assert result == expected_response

    def test_fix_lti_user_url_construction(self):
        """Test that the correct URL is constructed"""
        email = "user@example.com"

        self.client.fix_lti_user(email)

        call_args = self.requester.post.call_args
        expected_url = urljoin(self.base_url, '/api/lti-user-fix/')
        assert call_args[0][0] == expected_url

    def test_fix_lti_user_request_data_format(self):
        """Test that request data is formatted correctly"""
        email = "test@example.com"

        self.client.fix_lti_user(email)

        call_args = self.requester.post.call_args
        assert call_args[1]['json'] == {"email": email}