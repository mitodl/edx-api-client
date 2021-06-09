"""Course Detail API"""
from urllib.parse import urljoin

from .models import CourseDetail


# pylint: disable=too-few-public-methods
class CourseDetails(object):
    """
    API Client to interface with the course detail API.
    """
    def __init__(self, requester, base_url):
        self._requester = requester
        self._base_url = base_url

    def get_detail(self, course_id, username=None):
        """
        Fetches course details.

        Args:
            course_id (str): An edx course id.

        Returns:
            CourseDetail
        """
        # the request is done on behalf of the current logged in user
        # this only works if COURSE_ABOUT_VISIBILITIY_PERMISSION is not
        # set to staff, otherwise you need to pass in a username with
        # permissions.
        if not username:
            resp = self._requester.get(urljoin
                                       (self._base_url,
                                        '/api/courses/v1/courses/{course_key}'
                                        .format(course_key=course_id)))
        else:
            resp = self._requester.get(urljoin
                                       (self._base_url,
                                        '/api/courses/v1/courses/{course_key}/'
                                        '?username={username}'
                                        .format(course_key=course_id,
                                                username=username)))

        resp.raise_for_status()

        return CourseDetail(resp.json())
