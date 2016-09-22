"""
edX Enrollment REST API client class
"""
from six.moves.urllib.parse import urljoin  # pylint: disable=import-error

from .models import Enrollment, Enrollments


# pylint: disable=too-few-public-methods
class CourseEnrollments(object):
    """
    edX student enrollments client
    """

    enrollment_url = '/api/enrollment/v1/enrollment'

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
            urljoin(self.base_url, self.enrollment_url))
        resp.raise_for_status()
        return Enrollments(resp.json())

    def create_audit_student_enrollment(self, course_id):
        """
        Creates an audit enrollment for the user in a given course

        Args:
            course_id (str): an edX course id

        Returns:
            Enrollment: object representing the student enrollment in the provided course
        """
        audit_enrollment = {
            "mode": "audit",
            "course_details": {"course_id": course_id}
        }
        # the request is done in behalf of the current logged in user
        resp = self.requester.post(
            urljoin(self.base_url, self.enrollment_url),
            json=audit_enrollment
        )
        resp.raise_for_status()
        return Enrollment(resp.json())
