"""
Tests for the content of the __init__ module
"""
import json
import os
from unittest import TestCase
try:
    from mock import patch
except ImportError:
    from unittest.mock import patch

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

        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/enrollments_list.json')) as file_obj:
            cls.enrollments_list_json = json.loads(file_obj.read())

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

    @patch('edx_api.enrollments.CourseEnrollments._get_enrollments_list_page')
    def test_get_enrollments(self, mock_get_enrollments_list_page):
        """
        Test get_enrollments return all enrollments.
        """
        mock_get_enrollments_list_page.side_effect = [
            ([{}, {}], 'cursor'),
            ([{}, {}], 'cursor'),
            ([{}, {}], 'cursor'),
            ([{}, {}], None)
        ]
        enrollments = list(self.enrollment_client.get_enrollments())
        assert len(enrollments) == 8

    @requests_mock.mock()
    def test_get_enrollments_list(self, mock_req):
        """
        Test get enrollments call with pagination.
        """
        mock_req.register_uri(
            'GET',
            CourseEnrollments.enrollment_list_url,
            text=json.dumps({
                'previous': None,
                'results': self.enrollments_list_json[:2],
                'next': 'http://base_url/enrl/?cursor=next-cursor'
            }),
        )
        mock_req.register_uri(
            'GET',
            '{url}?cursor=next-cursor'.format(url=CourseEnrollments.enrollment_list_url),
            text=json.dumps({
                'previous': 'http://base_url/enrl/?cursor=next-cursor',
                'results': self.enrollments_list_json[2:],
                'next': None,
            })
        )
        enrollments = list(self.enrollment_client.get_enrollments())
        assert len(enrollments) == 4
