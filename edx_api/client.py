"""edX api client"""
# pylint: disable=fixme
import requests

from . import DEFAULT_TIME_OUT
from .bulk_user_retirement import BulkUserRetirement
from .ccx import CCX
from .certificates import UserCertificates
from .course_list import CourseList
from .course_detail import CourseDetails, CourseModes
from .course_runs import CourseRuns
from .course_structure import CourseStructure
from .enrollments import CourseEnrollments
from .email_settings import EmailSettings
from .grades import UserCurrentGrades
from .user_info import UserInfo
from .user_validation import UserValidation


class EdxApi:
    """
    A client for speaking with edX.
    """

    def __init__(
        self, credentials, base_url="https://courses.edx.org/", timeout=DEFAULT_TIME_OUT
    ):
        if "access_token" not in credentials:
            raise AttributeError(
                "Due to a lack of support for Client Credentials Grant in edX,"
                " you must specify the access token."
            )

        self.base_url = base_url
        self.credentials = credentials
        self.timeout = timeout

    def get_requester(self, token_type="Bearer"):
        """
        Returns an object to make authenticated requests. See python `requests` for the API.
        """
        # TODO(abrahms): Perhaps pull this out into a factory function for
        # generating an EdxApi instance with the proper requester & credentials.
        session = requests.session()
        session.headers.update(
            {
                "Authorization": f"{token_type} {self.credentials['access_token']}"
            }
        )

        old_request = session.request

        def patched_request(*args, **kwargs):
            """
            adds timeout param to session.request
            """
            return old_request(*args, timeout=self.timeout, **kwargs)

        session.request = patched_request
        return session

    @property
    def course_list(self):
        """Course List API"""
        return CourseList(self.get_requester(), self.base_url)

    @property
    def course_structure(self):
        """Course Structure API"""
        return CourseStructure(self.get_requester(), self.base_url)

    @property
    def course_detail(self):
        """Course Detail API"""
        return CourseDetails(self.get_requester(), self.base_url)

    @property
    def course_mode(self):
        """Course Detail API"""
        return CourseModes(self.get_requester(), self.base_url)

    @property
    def enrollments(self):
        """Course Enrollments API"""
        return CourseEnrollments(self.get_requester(), self.base_url)

    @property
    def ccx(self):
        """CCX API"""
        return CCX(self.get_requester(), self.base_url)

    @property
    def email_settings(self):
        """Email Settings API"""
        return EmailSettings(self.get_requester(), self.base_url)

    @property
    def certificates(self):
        """Certificates API"""
        return UserCertificates(self.get_requester(), self.base_url)

    @property
    def current_grades(self):
        """Current Grades API"""
        return UserCurrentGrades(self.get_requester(), self.base_url)

    @property
    def user_info(self):
        """User info API"""
        return UserInfo(self.get_requester(), self.base_url)

    @property
    def bulk_user_retirement(self):
        """Bulk user retirement API"""
        return BulkUserRetirement(self.get_requester(token_type="jwt"), self.base_url)

    @property
    def user_validation(self):
        """User validation API"""
        return UserValidation(self.get_requester(), self.base_url)

    @property
    def course_runs(self):
        """Course runs management API (Works with CMS)"""
        return CourseRuns(self.get_requester(token_type="jwt"), self.base_url)
