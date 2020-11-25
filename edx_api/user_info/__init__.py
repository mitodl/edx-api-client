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

    def update_user_name(self, username, user_full_name):
        """
        Updates Full-Name of the user

        Args:
            username (user.models.User): Username of the Application user
            user_full_name: Full name to be replace/updated with old full name

        Returns:
            UserInfo: Object with user details for whom the name is updated
        """
        user_name_data = dict(name=user_full_name)

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
            json=user_name_data)
        resp.raise_for_status()

        return Info(resp.json())
