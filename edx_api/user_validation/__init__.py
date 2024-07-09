"""Client for user_validation API"""
from urllib.parse import urljoin

from .models import Validation


class UserValidation(object):
    """
    edX user validation client
    """

    api_url = "/api/user/v1/validation/registration"

    def __init__(self, requester, base_url):
        """
        Args:
            requester (Requester): an unauthenticated objects for requests to edX
            base_url (str): string representing the base URL of an edX LMS instance
        """
        self.requester = requester
        self.base_url = base_url

    def validate_user_registration(self, registration_information=None):
        """
        Validate information about user data during registration.

        Args:
            registration_information (dict): request payload to validate name or username

        Returns:
            UserValidation: Object representing the user validation
        """
        resp = self.requester.post(
            urljoin(self.base_url, self.api_url), data=registration_information
        )
        resp.raise_for_status()

        return Validation(resp.json())
