"""Client for user_validation API"""
from urllib.parse import urljoin

from .models import UserValidationResult


class UserValidation(object):
    """
    Open edX user validation client
    """

    api_url = "/api/user/v1/validation/registration"

    def __init__(self, requester, base_url):
        """
        Args:
            requester (object): an unauthenticated object for request to Open edX
            base_url (str): string representing the base URL of an Open edX LMS instance
        """
        self.requester = requester
        self.base_url = base_url

    def validate_user_registration_info(self, registration_information=None):
        """
        Validate information about user data during registration.

        Args:
            registration_information (dict): request payload to validate user registration information
            i.e. name or username

        Returns:
            UserValidationResult: Object representing the user validation response data
        """
        resp = self.requester.post(
            urljoin(self.base_url, self.api_url), data=registration_information
        )
        resp.raise_for_status()

        return UserValidationResult(resp.json())
