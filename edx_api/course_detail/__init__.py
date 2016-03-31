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

    def get_detail(self, course_id):
        """
        Fetches course details.

        Args:
            course_id (str): An edx course id.

        Returns:
            CourseDetail
        """
        # the request is done in behalf of the current logged in user
        resp = self._requester.get(
            urljoin(
                self._base_url,
                '/api/courses/v1/courses/{course_key}/'.format(course_key=course_id)
            )
        )

        resp.raise_for_status()

        return CourseDetail(resp.json())
