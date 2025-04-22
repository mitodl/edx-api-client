"""
edX Course List REST API client class
"""
from urllib.parse import urljoin

from .models import Courses


class CourseList:
    """
    API Client to interface with the course list API.
    """

    course_list_url = '/api/courses/v1/courses/'

    def __init__(self, requester, base_url):
        """
        Args:
            requester (Requester): an authenticated objects for requests to edX
            base_url (str): string representing the base URL of an edX LMS instance
        """
        self._requester = requester
        self._base_url = base_url

    def get_courses(self, username=None, org=None, search_term=None, 
                   mobile_available=None, active_only=None, 
                   course_keys=None, page=None, page_size=None, **kwargs):
        """
        Get a list of courses visible to the specified user

        Args:
            username (str): Optional. The username of the specified user whose visible 
                           courses we want to see.
            search_term (str): Optional. Search term to filter courses
            active_only (bool): Optional. Only return courses that have not ended
            course_keys (list): Optional. List of course keys to retrieve

        Returns:
            Courses: Container for course list results
        """
        params = {}

        if username is not None:
            params['username'] = username
        if search_term is not None:
            params['search_term'] = search_term
        if active_only is not None:
            params['active_only'] = active_only
        if course_keys is not None:
            params['course_keys'] = course_keys

        params.update(kwargs)

        resp = self._requester.get(
            urljoin(self._base_url, self.course_list_url),
            params=params
        )

        resp.raise_for_status()
        resp_json = resp.json()
        results = resp_json['results']

        return Courses(results)
