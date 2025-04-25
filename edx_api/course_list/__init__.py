"""
edX Course List REST API client class
"""
from urllib.parse import urljoin

from .constants import PAGE_SIZE, BATCH_SIZE
from ..course_detail.models import CourseDetail


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
            params['page'] = page

            resp = self._requester.get(
                urljoin(self._base_url, self.course_list_url),
                params=params
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
        Get a list of courses visible to the specified user

        Args:
            course_keys (list): Optional. List of course keys to retrieve
            org (str): Optional. Filter by organization code (e.g., "HarvardX")
            search_term (str): Optional. Search term to filter courses
            username (str): Optional. The username whose visible courses to return
            active_only (bool): Optional. Only return non-ended courses
            **kwargs: Additional query parameters

        Notes:
            - Handles batching and pagination automatically
            - Returns a generator to process courses one at a time

        Returns:
            Generator yielding CourseDetail objects for each course
        """

        params = kwargs.copy()
        if org is not None:
            params['org'] = org
        if search_term is not None:
            params['search_term'] = search_term
        if username is not None:
            params['username'] = username
        if active_only is not None:
            params['active_only'] = active_only

        page_size = PAGE_SIZE
        params['page_size'] = page_size

        if course_keys:
            batch_size = BATCH_SIZE
            for i in range(0, len(course_keys), batch_size):
                batch = course_keys[i:i + batch_size]
                batch_params = params.copy()
                batch_params['course_keys'] = batch

                for course in self._get_paginated_courses(batch_params):
                    yield course
        else:
            for course in self._get_paginated_courses(params):
                yield course
