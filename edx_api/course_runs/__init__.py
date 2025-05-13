"""Course Runs API"""
from requests.exceptions import HTTPError
from urllib import parse
from .exceptions import CourseRunAPIError


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
        Clones a course run from source_course_id in Open edX.

        Args:
            source_course_id (str): An edx course id from which to clone the new run.
            destination_course_id (str): A course id to which to clone the new run from the destination.

        Returns:
            Response: The response from the Open edX API.
        Raises:
            CourseRunError: If the request to clone the course run fails.
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
            raise CourseRunAPIError(
                f"Failed to clone course run: {e.response.status_code} - {e.response.text}"
            ) from e

    def create_course_run(self, org, number, run, title):
        """
        Creates a new canonical course run in Open edX.

        Args:
            org (str): Organization for the new course run.
            number (str): Course number for the new course run.
            run (str): The run id for the new course run.
            title (str): The title of the new course run.

        Returns:
            Response: The response from the Open edX API.
        Raises:
            CourseRunError: If the request to clone the course run fails.
        """
        # the request is done on behalf of the staff user
        payload = {
            "org": org,
            "number": number,
            "run": run,
            "title": title,

        }
        resp = self._requester.post(
            parse.urljoin(self._base_url, "api/v1/course_runs/"), json=payload
        )
        try:
            resp.raise_for_status()
            return resp.json()
        except HTTPError as e:
            raise CourseRunAPIError(
                f"Failed to create course run: {e.response.status_code} - {e.response.text}"
            ) from e
