"""Course Runs API"""
from requests.exceptions import HTTPError
from urllib import parse
from .exceptions import CourseRunError


# pylint: disable=too-few-public-methods
class CourseRuns:
    """
    API Client to interact with the course runs API in Open edX CMS.
    """

    def __init__(self, requester, base_url):
        self._requester = requester
        self._base_url = base_url

    def clone_course_run(self, source_course_id, destination_course_id):
        """
        Clones a course in Open edX.

        Args:
            source_course_id (str): An edx course id from which to clone the new run.
            destination_course_id (str): A course id to which to clone the new run from the destination.

        Returns:
            CourseRun
        """
        # the request is done on behalf of the staff user
        payload = {
            "source_course_id": source_course_id,
            "destination_course_id": destination_course_id,
        }
        resp = self._requester.post(
            parse.urljoin(self._base_url, "api/v1/course_runs/clone/"), json=payload
        )
        try:
            resp.raise_for_status()
            return resp.json()
        except HTTPError as e:
            raise CourseRunError(
                f"Failed to clone course run: {e.response.status_code} - {e.response.text}"
            ) from e
