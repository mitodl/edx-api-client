"""Course Detail API"""
from six.moves.urllib.parse import urljoin  # pylint: disable=import-error

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
            username (str): an edx user's username

        Returns:
            CourseDetail
        """
        # The request may be done on behalf of the user (username) provided. Depending
        # on the way edX is set up, the course detail may be limited to `staff` only users.
        # Not specifying a username results in request being performed on behalf of
        # an AnonymousUser.
        url = urljoin(
            self._base_url,
            '/api/courses/v1/courses/{course_key}/'.format(course_key=course_id)
        )
        if username:
            url = '{url}?username={username}'.format(url=url, username=username)
        resp = self._requester.get(url)

        resp.raise_for_status()

        return CourseDetail(resp.json())
