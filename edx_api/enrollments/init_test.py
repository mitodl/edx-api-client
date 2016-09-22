"""
Tests for the content of the __init__ module
"""
import json
import os
from unittest import TestCase

import requests_mock
from six.moves.urllib.parse import urljoin  # pylint: disable=import-error

from edx_api.client import EdxApi
from edx_api.enrollments import CourseEnrollments


class EnrollmentsTest(TestCase):
    """
    Tests for the enrollments base function in the __init__ module
    """

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/user_enrollments.json')) as file_obj:
            cls.enrollments_json = json.loads(file_obj.read())

        cls.enrollment_json = cls.enrollments_json[0]
        base_edx_url = 'http://edx.example.com'
        cls.base_url = urljoin(base_edx_url, CourseEnrollments.enrollment_url)
        client = EdxApi({'access_token': 'foobar'}, cls.base_url)
        cls.enrollment_client = client.enrollments

    @requests_mock.mock()
    def test_create_enrollment(self, mock_req):
        """
        Tests the post request to create an enrollment.
        This just tests that the client expects a JSON object representing the enrollment.
        """
        mock_req.post(self.base_url, text=json.dumps(self.enrollment_json))
        enrollment = self.enrollment_client.create_audit_student_enrollment(
            self.enrollment_json['course_details']['course_id'])
        for key, val in enrollment.json.items():
            assert self.enrollment_json.get(key) == val
