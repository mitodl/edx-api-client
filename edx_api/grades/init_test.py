"""
Test handling of responses from grades api.
"""

import json
import os
from unittest import TestCase
from urllib.parse import urljoin

import requests_mock

from edx_api import enrollments, grades
from edx_api.client import EdxApi


class GradesApiTestCase(TestCase):
    """
    Test handling of mocked API responses in Grades API client.
    """

    base_url = "https://edx.example.com"

    def setUp(self):
        super(GradesApiTestCase, self).setUp()

        with open(
            os.path.join(
                os.path.dirname(__file__),
                "../enrollments/fixtures/user_enrollments.json",
            )
        ) as file:  # pylint: disable=redefined-builtin
            self.enrollment_data = json.load(file)
        self.enrollment_url = urljoin(
            "https://edx.example.com", enrollments.CourseEnrollments.enrollment_url
        )
        self.client = EdxApi({"access_token": "opensesame"}, "https://edx.example.com")

    @requests_mock.mock()
    def test_api_return_value(self, mock_req):
        """
        Verify that the object returned from the current_grades endpoints is a CurrentGrades.
        """
        mock_req.get(
            requests_mock.ANY,
            text=json.dumps(self.get_grades_data("course_grades_hawthorn.json")),
        )
        mock_req.get(self.enrollment_url, text=json.dumps(self.enrollment_data))
        response = self.client.current_grades.get_course_current_grades(
            "course-v1:edX+DemoX+Demo_Course"
        )
        assert isinstance(response, grades.CurrentGradesByCourse)

    @requests_mock.mock()
    def test_ironwood_api(self, mock_req):
        """
        Verify that the api can handle the ironwood version of the api.
        """
        mock_req.get(
            requests_mock.ANY,
            text=json.dumps(self.get_grades_data("course_grades_ironwood_p2.json")),
        )
        mock_req.get(self.enrollment_url, text=json.dumps(self.enrollment_data))
        grades_response = self.client.current_grades.get_course_current_grades(
            "course-v1:edX+DemoX+Demo_Course"
        )
        assert isinstance(grades_response, grades.CurrentGradesByCourse)
        self.assertEqual(len(grades_response.current_grades), 2)

    @requests_mock.mock()
    def test_paginated_ironwood_api(self, mock_req):
        """
        Verify that the ironwood api handles paginated data properly
        """
        mock_req.get(
            requests_mock.ANY,
            [
                {
                    "text": json.dumps(
                        self.get_grades_data("course_grades_ironwood_p1.json")
                    )
                },
                {
                    "text": json.dumps(
                        self.get_grades_data("course_grades_ironwood_p2.json")
                    )
                },
            ],
        )
        mock_req.get(self.enrollment_url, text=json.dumps(self.enrollment_data))
        grades_response = self.client.current_grades.get_course_current_grades(
            "course-v1:edX+DemoX+Demo_Course"
        )
        self.assertIsInstance(grades_response, grades.CurrentGradesByCourse)
        self.assertEqual(len(grades_response.current_grades), 4)

    @staticmethod
    def get_grades_data(filename):
        """
        Return the JSON data from the named fixture.
        """
        with open(
            os.path.join(os.path.dirname(__file__), "fixtures", filename)
        ) as file:  # pylint: disable=redefined-builtin
            return json.load(file)
