"""edX api client"""
# pylint: disable=fixme
from . import DEFAULT_TIME_OUT
from .ccx import CCX
from .certificates import UserCertificates
from .course_detail import CourseDetails
from .course_structure import CourseStructure
from .enrollments import CourseEnrollments
from .grades import UserCurrentGrades
from .requester import Requester
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

    @property
    def get_requester(self):
        """Returns an Requester object to make authenticated requests"""
        return Requester(self.timeout, self.credentials['access_token'])

    @property
    def course_structure(self):
        """Course Structure API"""
        return CourseStructure(self.get_requester, self.base_url)

    @property
    def course_detail(self):
        """Course Detail API"""
        return CourseDetails(self.get_requester, self.base_url)

    @property
    def enrollments(self):
        """Course Enrollments API"""
        return CourseEnrollments(self.get_requester, self.base_url)

    @property
    def ccx(self):
        """CCX API"""
        return CCX(self.get_requester, self.base_url)

    @property
    def certificates(self):
        """Certificates API"""
        return UserCertificates(self.get_requester, self.base_url)

    @property
    def current_grades(self):
        """Current Grades API"""
        return UserCurrentGrades(self.get_requester, self.base_url)

    @property
    def user_info(self):
        """User info API"""
        return UserInfo(self.get_requester, self.base_url)
