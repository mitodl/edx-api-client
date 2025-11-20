"""Client for LTI Tools API"""
from urllib.parse import urljoin


class LTITools:
    """
    Open edX LTI Tools client
    """

    def __init__(self, requester, base_url):
        """
        Args:
            requester (Requester): an authenticated objects for requests to edX
            base_url (str): string representing the base URL of an edX LMS instance
        """
        self.requester = requester
        self.base_url = base_url


    def fix_lti_user(self, email):
        """
        Fixes an LTI user with duplicate email

        Args:
            email (str): Email of the Application user

        Returns:
            bool: True if the user was fixed successfully, False otherwise
        """
        request_data = {"email": email}

        # the request is done on behalf of the current logged in user
        return self.requester.post(
            urljoin(
                self.base_url,
                '/api/lti-user-fix/'
            ),
            json=request_data)
