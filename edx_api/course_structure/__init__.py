"""Course Structure API"""
from urllib.parse import urljoin

from .models import Structure


class CourseStructure(object):
    """
    API Client to interface with the course structure API.
    """
    def __init__(self, requester, base_url):
        self.requester = requester
        self.base_url = base_url

    def course_blocks(self, course_id, username):
        """
        Fetches course blocks.

        Args:
            course_id (str): An edx course id.
            username (str): username of the user to query for (can reveal hidden
                            modules)

        Returns:
            Structure
        """
        resp = self.requester.get(
            urljoin(self.base_url, '/api/courses/v1/blocks/'),
            params={
                "depth": "all",
                "username": username,
                "course_id": course_id,
                "requested_fields": "children,display_name,id,type,visible_to_staff_only",
            })

        resp.raise_for_status()

        return Structure(resp.json())
