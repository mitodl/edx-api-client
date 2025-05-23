"""
Tests for the content of the __init__ module in course_runs
"""

import json
import os

import pytest
import requests_mock

from unittest import TestCase
from urllib.parse import urljoin

from edx_api.client import EdxApi
from edx_api.course_runs import CourseRuns


class CourseRunsTest(TestCase):
    """
    Tests for the course runs API base function in the __init__ module
    """

    @classmethod
    def setUpClass(cls):
        with open(
            os.path.join(os.path.dirname(__file__), "fixtures/course_run.json")
        ) as file_obj:
            cls.course_run_json = json.loads(file_obj.read())

        with open(
            os.path.join(os.path.dirname(__file__), "fixtures/course_run_list.json")
        ) as file_obj:
            cls.course_run_list_json = json.loads(file_obj.read())
        cls.course_run_clone_json = {"message": "Course cloned successfully"}

        cls.course_run_responses = [
            {"json": cls.course_run_json, "status_code": 201},
            {"json": cls.course_run_clone_json, "status_code": 201},
            {"json": cls.course_run_list_json, "status_code": 200},
        ]

        base_edx_url = "http://studio.local.openedx.io"
        cls.course_run_url = urljoin(base_edx_url, CourseRuns.course_run_url)
        cls.course_run_clone_url = urljoin(
            base_edx_url, CourseRuns.course_run_clone_url
        )
        cls.client = EdxApi({"access_token": "foobar"}, base_edx_url)
        cls.course_run_client = cls.client.course_runs

    @requests_mock.mock()
    def test_clone_course_run(self, mock_req):
        """
        Tests the POST request to clone a course run.
        """
        mock_req.post(self.course_run_clone_url, **self.course_run_responses[1])
        response = self.course_run_client.clone_course_run(
            source_course_id="test", destination_course_id="test1"
        )
        assert response.json() == self.course_run_responses[1]["json"]

    @requests_mock.mock()
    def test_create_course_run(self, mock_req):
        """
        Tests the POST request to create a course run.
        """
        mock_req.post(self.course_run_url, **self.course_run_responses[0])
        response = self.course_run_client.create_course_run(
            org="ORG", number="NUMBER", run="RUN", title="Test Course"
        )
        assert response.json == self.course_run_responses[0]["json"]
        # Check that start and end are passed together otherwise none passed at all
        with pytest.raises(ValueError):
            self.course_run_client.create_course_run(
                org="ORG",
                number="NUMBER",
                run="RUN",
                title="Test Course",
                start="2023-01-01T00:00:00Z",
            )
        with pytest.raises(ValueError):
            self.course_run_client.create_course_run(
                org="ORG",
                number="NUMBER",
                run="RUN",
                title="Test Course",
                end="2023-01-01T00:00:00Z",
            )

    @requests_mock.mock()
    def test_update_course_run(self, mock_req):
        """
        Tests the PUT request to update a course run.
        """
        course_id = "course-v1:ORG+NUMBER+RUN"
        url = self.course_run_url + f"{course_id}/"
        mock_req.put(url, **self.course_run_responses[0])
        response = self.course_run_client.update_course_run(
            course_id=course_id, title="Updated Title", pacing_type="self_paced"
        )
        assert response.json == self.course_run_responses[0]["json"]
        # Check that start and end are passed together otherwise none passed at all
        with pytest.raises(ValueError):
            self.course_run_client.update_course_run(
                course_id=course_id, title="Updated Title", start="2023-01-01T00:00:00Z"
            )
        with pytest.raises(ValueError):
            self.course_run_client.update_course_run(
                course_id=course_id, title="Updated Title", end="2023-01-01T00:00:00Z"
            )

    @requests_mock.mock()
    def test_get_course_run(self, mock_req):
        """
        Tests the GET request to get a single create a course run based on course ID.
        """
        course_id = "course-v1:ORG+NUMBER+RUN"
        url = self.course_run_url + f"{course_id}/"
        mock_req.get(url, **self.course_run_responses[0])
        response = self.course_run_client.get_course_run(course_id=course_id)
        assert response.json == self.course_run_responses[0]["json"]

    @requests_mock.mock()
    def test_get_course_run_list(self, mock_req):
        """
        Tests the GET request to get the list of courser runs.
        """
        url = self.course_run_url
        mock_req.get(url, **self.course_run_responses[2])
        response = self.course_run_client.get_course_runs_list()
        assert response.json == self.course_run_responses[2]["json"]
