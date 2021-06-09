"""
edX Certificates REST API client class
"""
from requests.exceptions import HTTPError
from urllib.parse import urljoin

from edx_api.enrollments import CourseEnrollments
from .models import Certificate, Certificates


class UserCertificates(object):
    """
    edX student certificates client
    """

    def __init__(self, requester, base_url):
        """
        Args:
            requester (Requester): an authenticated objects for requests to edX
            base_url (str): string representing the base URL of an edX LMS instance
        """
        self.requester = requester
        self.base_url = base_url

    def get_student_certificate(self, username, course_id):
        """
        Returns an Certificate object with the user certificates

        Args:
            username (str): an edx user's username
            course_id (str): an edX course id.

        Returns:
            Certificate: object representing the student certificate for a course
        """
        # the request is done in behalf of the current logged in user
        resp = self.requester.get(
            urljoin(
                self.base_url,
                '/api/certificates/v0/certificates/{username}/courses/{course_key}/'.format(
                    username=username,
                    course_key=course_id
                )
            )
        )

        resp.raise_for_status()

        return Certificate(resp.json())

    def get_student_certificates(self, username, course_ids=None):
        """
        Returns an Certificates object with the user certificates

        Args:
            username (str): an edx user's username
            course_ids (list): a list of edX course ids.

        Returns:
            Certificates: object representing the student certificates for a course
        """
        # if no course ids are provided, let's get the user enrollments
        if course_ids is None:
            enrollments_client = CourseEnrollments(self.requester, self.base_url)
            enrollments = enrollments_client.get_student_enrollments()
            course_ids = list(enrollments.get_enrolled_course_ids())

        all_certificates = []
        for course_id in course_ids:
            try:
                all_certificates.append(self.get_student_certificate(username, course_id))
            except HTTPError as error:
                if error.response.status_code >= 500:
                    raise

        return Certificates(all_certificates)
