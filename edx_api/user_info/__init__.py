"""Client for user_info API"""
from urllib.parse import urljoin

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

    def update_user_name(self, username, full_name):
        """
        Updates full name of the user

        Args:
            username (str): Username of the Application user
            full_name (str): Full name that will replace the user's existing full name

        Returns:
            UserInfo: Object representing the edX user
        """
        request_data = dict(name=full_name)

        # the request is done on behalf of the current logged in user
        self.requester.headers.update(
            {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/merge-patch+json",
            }
        )
        resp = self.requester.patch(
            urljoin(
                self.base_url,
                '/api/user/v1/accounts/{username}'.format(username=username)
            ),
            json=request_data)
        resp.raise_for_status()

        return Info(resp.json())
