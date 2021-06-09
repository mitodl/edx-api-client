"""
edX Enrollment REST API client class
"""
from edx_api.constants import ENROLLMENT_MODE_AUDIT

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs
from urllib.parse import urljoin

from .models import Enrollment, Enrollments


# pylint: disable=too-few-public-methods
class CourseEnrollments(object):
    """
    edX student enrollments client
    """

    enrollment_url = '/api/enrollment/v1/enrollment'
    enrollment_list_url = '/api/enrollment/v1/enrollments'

    def __init__(self, requester, base_url):
        """
        Args:
            requester (Requester): an authenticated objects for requests to edX
            base_url (str): string representing the base URL of an edX LMS instance
        """
        self.requester = requester
        self.base_url = base_url

    def _get_enrollments_list_page(self, params=None):
        """
        Submit request to retrieve enrollments list.

        Args:
            params (dict): Query parameters to use in the request. Valid parameters are:
                * course_id: Filters the result to course enrollments for the course
                    corresponding to the given course ID. The value must be URL encoded.
                    Optional.
                * username: username: List of comma-separated usernames. Filters the result to the
                    course enrollments of the given users. Optional.
        """
        req_url = urljoin(self.base_url, self.enrollment_list_url)
        resp = self.requester.get(req_url, params=params)
        resp.raise_for_status()
        resp_json = resp.json()
        results = resp_json['results']
        next_url_str = resp_json.get('next')
        cursor = None
        qstr_cursor = None
        if next_url_str:
            next_url = urlparse(next_url_str)
            qstr = parse_qs(next_url.query)
            qstr_cursor = qstr.get('cursor')

        if qstr_cursor and isinstance(qstr_cursor, list):
            cursor = qstr_cursor[0]

        return results, cursor

    def get_enrollments(self, course_id=None, usernames=None):
        """
        List all course enrollments.

        Args:
            course_id (str, optional): If used enrollments will be filtered to the specified
                course id.
            usernames (list, optional): List of usernames to filter enrollments.

        Notes:
            - This method returns an iterator to avoid going through the entire pagination at once.
            - The :class:`Enrollments` instance returned for each generated item will not have any
                course details.

        Examples:
            Get all enrollments for a specific course id
            >>> api = EdxApi({'access_token': 'token'}, 'http://base_url')
            >>> enrollments = api.enrollments.get_enrollments(course_id='course_id')
            >>> for enrollment in enrollments:
                    do_something(enrollment)

            Get all enrollments for a set of usernames
            >>> api = EdxApi({'access_token': 'token'}, 'http://base_url')
            >>> enrollments = api.enrollments.get_enrollments(usernames=['user1', 'user2'])
            >>> for enrollment in enrollments:
                    do_something(enrollment)

        Returns:
            Generator with an instance of :class:`Enrollments` for each item.
        """
        params = {}
        if course_id is not None:
            params['course_id'] = course_id
        if usernames is not None and isinstance(usernames, list):
            params['username'] = ','.join(usernames)

        done = False
        while not done:
            enrollments, next_cursor = self._get_enrollments_list_page(params)
            for enrollment in enrollments:
                yield Enrollment(enrollment)

            if next_cursor:
                params['cursor'] = next_cursor
            else:
                done = True

    def get_student_enrollments(self):
        """
        Returns an Enrollments object with the user enrollments for the user
        whose access token was provided to the API client.

        Returns:
            Enrollments: object representing the student enrollments
        """
        resp = self.requester.get(
            urljoin(self.base_url, self.enrollment_url))
        resp.raise_for_status()
        return Enrollments(resp.json())

    def create_student_enrollment(
            self,
            course_id,
            mode=ENROLLMENT_MODE_AUDIT,
            username=None,
            enrollment_attributes=None
    ):
        """
        Creates an enrollment for the user in a given course

        Args:
            course_id (str): an edX course id.
            mode (str): Enrollment mode.
            username (str): Username.
            enrollment_attributes (dict): Enrollment attributes, which are added directly to
                                            the request body.
                                          If specified, the following keys are expected:
                                          - namespace,
                                          - name,
                                          - value.

        Returns:
            Enrollment: object representing the student enrollment in the provided course
        """
        enrollment_data = {
            "mode": mode,
            "course_details": {"course_id": course_id}
        }
        if username:
            enrollment_data['user'] = username
        if enrollment_attributes:
            enrollment_data['enrollment_attributes'] = enrollment_attributes
        # the request is done in behalf of the current logged in user
        resp = self.requester.post(
            urljoin(self.base_url, self.enrollment_url),
            json=enrollment_data
        )
        resp.raise_for_status()
        return Enrollment(resp.json())

    def create_audit_student_enrollment(self, course_id, username=None):
        """
        Creates an audit enrollment for the user in a given course

        Args:
            course_id (str): An edX course id.
            username (str): Username.

        Returns:
            Enrollment: object representing the student enrollment in the provided course
        """
        return self.create_student_enrollment(
            course_id,
            mode=ENROLLMENT_MODE_AUDIT,
            username=username
        )

    def deactivate_enrollment(self, course_id):
        """
        Deactivates an enrollment in the given course for the user
        whose access token was provided to the API client (in other words, the
        user will be unenrolled)

        Args:
            course_id (str): An edX course id.

        Returns:
            Enrollment: object representing the deactivated student enrollment
        """
        resp = self.requester.post(
            urljoin(self.base_url, self.enrollment_url),
            json={
                "course_details": {"course_id": course_id},
                "is_active": False,
            }
        )
        resp.raise_for_status()
        return Enrollment(resp.json())
