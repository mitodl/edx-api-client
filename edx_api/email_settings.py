"""
API client for interacting with change email settings
"""
import logging
from urllib import parse

log = logging.getLogger(__name__)


class EmailSettings(object):
    """
    API client for interacting with email settings
    """
    api_url = "/api/change_email_settings"

    def __init__(self, requester, base_url):
        self.requester = requester
        self.base_url = base_url

    def change_settings(self, payload):
        """
        Execute the client request to edX endpoint
        Args:
            payload (dict): request payload
        Returns:
            JSON response (dict)
        """
        response = self.requester.post(
            parse.urljoin(self.base_url, self.api_url),
            json=payload
        )

        try:
            response.raise_for_status()
        except Exception:
            log.error(response.json())
        return response.json().get("success", False)

    def subscribe(self, course_id):
        """
        Subscribe the user to receive all course emails
        Args:
            course_id (int): Corresponding edx course id
        """
        payload = {
            "course_id": course_id,
            "receive_emails": "on",
        }
        return self.change_settings(payload)

    def unsubscribe(self, course_id):
        """
        Unsubscribe the user from receiving course emails
        Args:
            course_id (int): Corresponding edx course
        """
        payload = {
            "course_id": course_id,
        }
        return self.change_settings(payload)
