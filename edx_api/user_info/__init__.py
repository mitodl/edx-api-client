"""Client for user_info API"""
from six.moves.urllib.parse import urljoin  # pylint: disable=import-error

from .models import Info


class UserInfo(object):
    """
    edX user info client
    """

    def __init__(self, requester, base_url):
        """
        Args:
            requester (Requester): an authenticated objects for requests to edX
            base_url (str): string representing the base URL of an edX LMS instance
        """
        self.requester = requester
        self.base_url = base_url

    def get_user_info(self):
        """
        Returns a UserInfo object for the logged in user.

        Returns:
            UserInfo: object representing the student current grades
        """
        # the request is done in behalf of the current logged in user
        resp = self.requester.get(
            urljoin(
                self.base_url,
                '/api/mobile/v0.5/my_user_info'
            )
        )

        resp.raise_for_status()

        return Info(resp.json())
