"""Course Runs API"""
from requests.exceptions import HTTPError
from urllib import parse
from .exceptions import CourseRunAPIError
from .models import CourseRun, CourseRunList


# pylint: disable=too-few-public-methods
class CourseRuns:
    """
    API Client to interact with the course runs API in Open edX CMS.
    """

    def __init__(self, requester, base_url):
        self._requester = requester
        self._base_url = base_url

    def _verify_and_generate_schedule(self, start, end, enrollment_start, enrollment_end):
        """
        Verifies and builds the schedule dictionary for course run creation.

        Args:
            start (datetime): The start date for the course run.
            end (datetime): The end date for the course run.
            enrollment_start (datetime): The enrollment start date for the course run.
            enrollment_end (datetime): The enrollment end date for the course run.

        Returns:
            dict: A dictionary containing the schedule information.
        """

        # All the date fields will be added in a sub-dictionary named "schedule".
        # If we want to update the schedule of the course, the start and end dates
        # are required by the API.
        if start or end:
            if not (start and end):
                raise ValueError("Both start and end dates must be provided if one is provided.")

            schedule = {
                "start": start.isoformat(),
                "end": end.isoformat(),
            }
            if enrollment_start:
                schedule["enrollment_start"] = enrollment_start.isoformat()
            if enrollment_end:
                schedule["enrollment_end"] = enrollment_end.isoformat()
            return schedule
        return None

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

    def create_course_run(self, org, number, run, title, pacing_type=None, start=None, end=None, enrollment_start=None, enrollment_end=None):
        """
        Creates a new canonical course run in Open edX.

        Args:
            org (str): Organization for the new course run.
            number (str): Course number for the new course run. (Without 'course-v1')
            run (str): The run id for the new course run.
            title (str): The title of the new course run.
            pacing_type (str, optional): The pacing type for the new course run. Defaults to None.
            start (datetime, optional): The start date for the new course run. Defaults to None.
            end (datetime, optional): The end date for the new course run. Defaults to None.
            enrollment_start (datetime, optional): The enrollment start date for the new course run. Defaults to None.
            enrollment_end (datetime, optional): The enrollment end date for the new course run. Defaults to None.

        Returns:
            CourseRun: The course run fields from the Open edX API.
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
        if pacing_type:
            payload["pacing_type"] = pacing_type

        # All the date fields should be added in a sub-dictionary named "schedule" inside the payload.
        schedule = self._verify_and_generate_schedule(
            start, end, enrollment_start, enrollment_end
        )
        if schedule:
            payload["schedule"] = schedule

        resp = self._requester.post(
            parse.urljoin(self._base_url, "api/v1/course_runs/"), json=payload
        )
        try:
            resp.raise_for_status()
            return CourseRun(resp.json())
        except HTTPError as e:
            raise CourseRunAPIError(
                f"Failed to create course run: {e.response.status_code} - {e.response.text}"
            ) from e

    def update_course_run(self, course_id, title=None, pacing_type=None, start=None, end=None, enrollment_start=None, enrollment_end=None):
        """
        Creates a new canonical course run in Open edX.

        Args:
            course_id (str): Course Id for the course run to update.
            title (str, optional): The title of the new course run.
            pacing_type (str, optional): The pacing type for the new course run. Defaults to None.
            start (datetime, optional): The start date for the new course run. Defaults to None.
            end (datetime, optional): The end date for the new course run. Defaults to None.
            enrollment_start (datetime, optional): The enrollment start date for the new course run. Defaults to None.
            enrollment_end (datetime, optional): The enrollment end date for the new course run. Defaults to None.

        Returns:
            CourseRun: The course run object containing the fields data from the Open edX API.
        Raises:
            CourseRunError: If the request to clone the course run fails.
        """
        # the request is done on behalf of the staff user
        payload = {}
        if title:
            payload["title"] = title
        if pacing_type:
            payload["pacing_type"] = pacing_type

        # All the date fields should be added in a sub-dictionary named "schedule" inside the payload.
        schedule = self._verify_and_generate_schedule(
            start, end, enrollment_start, enrollment_end
        )
        if schedule:
            payload["schedule"] = schedule

        resp = self._requester.put(
            parse.urljoin(self._base_url, f"api/v1/course_runs/{course_id}/"), json=payload
        )
        try:
            resp.raise_for_status()
            return CourseRun(resp.json())
        except HTTPError as e:
            raise CourseRunAPIError(
                f"Failed to update course run: {e.response.status_code} - {e.response.text}"
            ) from e

    def get_course_runs_list(self, page_url=None):
        """
        Returns a list of course runs in Open edX.

        Args:
            page_url (str, optional): The URL for the next or previous page of course runs. Defaults to None.
            If not provided, the first page of course runs will be fetched.

        Returns:
            list: A list of course run objects.
        Raises:
            CourseRunError: If the request to clone the course run fails.
        """
        resp = self._requester.get(
            page_url or parse.urljoin(self._base_url, "api/v1/course_runs/")
        )
        try:
            resp.raise_for_status()
            return CourseRunList(resp.json())
        except HTTPError as e:
            raise CourseRunAPIError(
                f"Failed to get course run list: {e.response.status_code} - {e.response.text}"
            ) from e

    def get_course_run(self, course_id):
        """
        Returns a course run object in Open edX.
        Args:
            course_id (str): The course id for the course run to get.
        Returns:
            CourseRun: The course run object.
        Raises:
            CourseRunError: If the request to clone the course run fails.
        """
        resp = self._requester.get(
            parse.urljoin(self._base_url, f"api/v1/course_runs/{course_id}/")
        )
        try:
            resp.raise_for_status()
            return CourseRun(resp.json())
        except HTTPError as e:
            raise CourseRunAPIError(
                f"Failed to get course run: {e.response.status_code} - {e.response.text}"
            ) from e