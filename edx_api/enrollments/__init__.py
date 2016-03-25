"""
edX Enrollment REST API client class
"""
from six.moves.urllib.parse import urljoin  # pylint: disable=import-error

from .models import Enrollments


# pylint: disable=too-few-public-methods
class CourseEnrollments(object):
    """
    edX student enrollments client
    """

    def __init__(self, requester, base_url):
        """
        Args:
            requester (Requester): an authenticated objects for requests to edX
            base_url (str): string representing the base URL of an edX LMS instance
        """
        self.requester = requester
        self.base_url = base_url

    def get_student_enrollments(self):
        """
        Returns an Enrollments object with the user enrollments

        Returns:
            Enrollments: object representing the student enrollments
        """
        # the request is done in behalf of the current logged in user
        resp = self.requester.get(
            urljoin(self.base_url, '/api/enrollment/v1/enrollment'))

        resp.raise_for_status()

        return Enrollments(resp.json())
