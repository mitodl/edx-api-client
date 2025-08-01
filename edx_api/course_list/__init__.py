"""
edX Course List REST API client class
"""
from urllib.parse import urljoin

from .constants import PAGE_SIZE, BATCH_SIZE
from edx_api.course_detail.models import CourseDetail


class CourseList:
    """
    API Client to interface with the course list API.
    """

    course_list_url = '/api/courses/v1/courses/'

    def __init__(self, requester, base_url):
        """
        Args:
            requester (Requester): an authenticated client for requests to edX
            base_url (str): string representing the base URL of an edX LMS instance
        """
        self._requester = requester
        self._base_url = base_url

    def _get_paginated_courses(self, params):
        """
        Helper method to handle pagination for a single API request.

        Args:
            params (dict): Query parameters for the API request

        Yields:
            CourseDetail: Course objects one at a time
        """
        page = 1
        while True:
            request_params = params.copy()
            request_params['page'] = page

            resp = self._requester.get(
                urljoin(self._base_url, self.course_list_url),
                params=request_params
            )
            resp.raise_for_status()

            data = resp.json()
            for course_data in data.get('results', []):
                yield CourseDetail(course_data)

            if data.get('pagination', {}).get('next'):
                page += 1
            else:
                break

    def get_courses(self, course_keys=None, org=None, search_term=None,
                    username=None, active_only=None, **kwargs):
        """
        Get a list of courses

        Retrieves course information from the edX Course List API with support for
        filtering, batching, and pagination. Returns courses as a generator to
        handle large datasets efficiently

        Args:
            course_keys (list, optional): List of course keys to retrieve.
            org (str, optional): Filter by organization code (e.g., "MIT").
            search_term (str, optional): Search term to filter courses.
            username (str, optional): The username whose visible courses to return.
            active_only (bool, optional): Only return non-ended courses.
            **kwargs: Additional query parameters

        Returns:
            Generator yielding CourseDetail objects for each course
        """

        params = kwargs.copy()
        params.update({
            'org': org,
            'search_term': search_term,
            'username': username,
            'active_only': active_only
        })
        params = {
            key: value for key, value in params.items()
            if value or (key == 'active_only' and value is not None)
        }

        params['page_size'] = PAGE_SIZE

        if course_keys:
            for start_index in range(0, len(course_keys), BATCH_SIZE):
                batch = course_keys[start_index:start_index + BATCH_SIZE]
                batch_params = params.copy()
                batch_params['course_keys'] = batch

                for course in self._get_paginated_courses(batch_params):
                    yield course
        else:
            for course in self._get_paginated_courses(params):
                yield course
