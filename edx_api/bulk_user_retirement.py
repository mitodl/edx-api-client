"""
API client for interacting with user retirement API
"""
import logging
from urllib import parse

log = logging.getLogger(__name__)


class BulkUserRetirement(object):
    """
    API client for interacting with user retirement API
    """

    api_url = "v1/accounts/bulk_retire_users"

    def __init__(self, requester, base_url):
        self.requester = requester
        self.base_url = base_url

    def retire_users(self, payload):
        """
        Execute the client request to edX endpoint

        Args:
            payload (dict): request payload

        Returns:
            JSON response (dict)
        """
        response = self.requester.post(
            parse.urljoin(self.base_url, self.api_url), json=payload
        )

        response.raise_for_status()
        return response.json()
