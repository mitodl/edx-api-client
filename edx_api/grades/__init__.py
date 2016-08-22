"""
edX Grades REST API client class
"""
from requests.exceptions import HTTPError
from six.moves.urllib.parse import urljoin  # pylint: disable=import-error

from edx_api.enrollments import CourseEnrollments
from .models import CurrentGrade, CurrentGrades


class UserCurrentGrades(object):
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

    def get_student_current_grade(self, username, course_id):
        """
        Returns an CurrentGrade object for the user in a course

        Args:
            username (str): an edx user's username
            course_id (str): an edX course id.

        Returns:
            CurrentGrade: object representing the student current grade for a course
        """
        # the request is done in behalf of the current logged in user
        resp = self.requester.get(
            urljoin(
                self.base_url,
                '/api/grades/v0/course_grade/{course_key}/users/?username={username}'.format(
                    username=username,
                    course_key=course_id
                )
            )
        )

        resp.raise_for_status()

        return CurrentGrade(resp.json()[0])

    def get_student_current_grades(self, username, course_ids=None):
        """
        Returns a CurrentGrades object with the user current grades.

        Args:
            username (str): an edx user's username
            course_ids (list): a list of edX course ids.

        Returns:
            CurrentGrades: object representing the student current grades
        """
        # if no course ids are provided, let's get the user enrollments
        if course_ids is None:
            enrollments_client = CourseEnrollments(self.requester, self.base_url)
            enrollments = enrollments_client.get_student_enrollments()
            course_ids = list(enrollments.get_enrolled_course_ids())

        all_current_grades = []
        for course_id in course_ids:
            try:
                all_current_grades.append(self.get_student_current_grade(username, course_id))
            except HTTPError as error:
                if error.response.status_code >= 500:
                    raise

        return CurrentGrades(all_current_grades)
