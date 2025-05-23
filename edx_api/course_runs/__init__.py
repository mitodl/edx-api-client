"""Course Runs API"""

from urllib import parse

from requests.exceptions import HTTPError

from .exceptions import CourseRunAPIError
from .models import CourseRun, CourseRunList


class CourseRuns:
    """
    API Client to interact with the course runs API in Open edX CMS.
    """

    course_run_url = "api/v1/course_runs/"
    course_run_clone_url = "api/v1/course_runs/clone/"

    def __init__(self, requester, base_url):
        self._requester = requester
        self._base_url = base_url

    def _verify_and_generate_schedule(
        self, start, end, enrollment_start, enrollment_end
    ):
        """
        Verifies and builds the schedule dictionary for course run create/update payload.

        Args:
            start (datetime): The start date for the course run.
            end (datetime): The end date for the course run.
            enrollment_start (datetime): The enrollment start date for the course run.
            enrollment_end (datetime): The enrollment end date for the course run.

        Returns:
            dict or None: A dictionary containing the schedule information or None.
        """

        # It is required by the Open edX that start and end dates are both present when a reschedule is requested.
        if start or end:
            if not (start and end):
                raise ValueError(
                    "Both start and end dates must be provided if one is provided."
                )

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
            destination_course_id (str): A course id for the new course run to be created.

        Returns:
            Response: The response from the Open edX API.
        Raises:
            CourseRunError: If the request to clone the course run fails.
        """

        payload = {
            "source_course_id": source_course_id,
            "destination_course_id": destination_course_id,
        }
        resp = self._requester.post(
            parse.urljoin(self._base_url, self.course_run_clone_url), json=payload
        )
        try:
            resp.raise_for_status()
            return resp
        except HTTPError as ex:
            raise CourseRunAPIError(
                f"Failed to clone course run: {ex.response.status_code} - {ex.response.text}"
            ) from ex

    def create_course_run(
        self,
        org,
        number,
        run,
        title,
        pacing_type=None,
        start=None,
        end=None,
        enrollment_start=None,
        enrollment_end=None,
    ):
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
            CourseRun: The course run response keys from the Open edX API.
        Raises:
            CourseRunError: If the request to create the course run fails.
        """
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
            parse.urljoin(self._base_url, self.course_run_url), json=payload
        )
        try:
            resp.raise_for_status()
            return CourseRun(resp.json())
        except HTTPError as ex:
            raise CourseRunAPIError(
                f"Failed to create course run: {ex.response.status_code} - {ex.response.text}"
            ) from ex

    def update_course_run(
        self,
        course_id,
        title=None,
        pacing_type=None,
        start=None,
        end=None,
        enrollment_start=None,
        enrollment_end=None,
    ):
        """
        Updates a course run in Open edX based on course_id.

        Args:
            course_id (str): Course Id for the course run to update. (Used for lookup)

            The following parameters are optional and can be used to update the course run:

            title (str, optional): The title of the new course run.
            pacing_type (str, optional): The pacing type for the new course run. Defaults to None.
            start (datetime, optional): The start date for the new course run. Defaults to None.
            end (datetime, optional): The end date for the new course run. Defaults to None.
            enrollment_start (datetime, optional): The enrollment start date for the new course run. Defaults to None.
            enrollment_end (datetime, optional): The enrollment end date for the new course run. Defaults to None.

        Returns:
            CourseRun: The course run object containing the fields from the Open edX API.
        Raises:
            CourseRunError: If the request to update the course run fails.
        """
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
            parse.urljoin(self._base_url, f"{self.course_run_url}/{course_id}/"),
            json=payload,
        )
        try:
            resp.raise_for_status()
            return CourseRun(resp.json())
        except HTTPError as ex:
            raise CourseRunAPIError(
                f"Failed to update course run: {ex.response.status_code} - {ex.response.text}"
            ) from ex

    def get_course_run(self, course_id):
        """
        Returns a course run object in Open edX.

        Args:
            course_id (str): The course id for the course run to get.
        Returns:
            CourseRun: The course run object.
        Raises:
            CourseRunError: If the request to get the course run fails.
        """
        resp = self._requester.get(
            parse.urljoin(self._base_url, f"{self.course_run_url}{course_id}/")
        )
        try:
            resp.raise_for_status()
            return CourseRun(resp.json())
        except HTTPError as ex:
            raise CourseRunAPIError(
                f"Failed to get course run: {ex.response.status_code} - {ex.response.text}"
            ) from ex

    def get_course_runs_list(self, page_url=None):
        """
        Returns a list of course runs in Open edX.

        Args:
            page_url (str, optional): The URL for the next or previous page of course runs. Defaults to None.
            If not provided, the first page of course runs will be fetched.

        Returns:
            list: A list of course run objects.
        Raises:
            CourseRunError: If the request to get the course runs list fails.
        """
        resp = self._requester.get(
            page_url or parse.urljoin(self._base_url, self.course_run_url)
        )
        try:
            resp.raise_for_status()
            return CourseRunList(resp.json())
        except HTTPError as ex:
            raise CourseRunAPIError(
                f"Failed to get course runs list: {ex.response.status_code} - {ex.response.text}"
            ) from ex
