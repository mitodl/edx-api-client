"""edX api client"""
# pylint: disable=fixme
import requests

from . import DEFAULT_TIME_OUT
from .ccx import CCX
from .certificates import UserCertificates
from .course_detail import CourseDetails
from .course_structure import CourseStructure
from .enrollments import CourseEnrollments
from .email_settings import EmailSettings
from .grades import UserCurrentGrades
from .user_info import UserInfo


class EdxApi(object):
    """
    A client for speaking with edX.
    """
    def __init__(self, credentials, base_url='https://courses.edx.org/', timeout=DEFAULT_TIME_OUT):
        if 'access_token' not in credentials:
            raise AttributeError(
                "Due to a lack of support for Client Credentials Grant in edX,"
                " you must specify the access token."
            )

        self.base_url = base_url
        self.credentials = credentials
        self.timeout = timeout

    def get_requester(self):
        """
        Returns an object to make authenticated requests. See python `requests` for the API.
        """
        # TODO(abrahms): Perhaps pull this out into a factory function for
        # generating an EdxApi instance with the proper requester & credentials.
        session = requests.session()
        session.headers.update({
            'Authorization': 'Bearer {}'.format(self.credentials['access_token']),
            'X-EdX-Api-Key': self.credentials.get('api_key'),
        })

        old_request = session.request

        def patched_request(*args, **kwargs):
            """
            adds timeout param to session.request
            """
            return old_request(*args, timeout=self.timeout, **kwargs)

        session.request = patched_request
        return session

    @property
    def course_structure(self):
        """Course Structure API"""
        return CourseStructure(self.get_requester(), self.base_url)

    @property
    def course_detail(self):
        """Course Detail API"""
        return CourseDetails(self.get_requester(), self.base_url)

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
