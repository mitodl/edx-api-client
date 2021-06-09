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
from urllib.parse import urljoin

from edx_api.client import EdxApi
from edx_api.constants import ENROLLMENT_MODE_AUDIT, ENROLLMENT_MODE_VERIFIED
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

        cls.enrollment_responses = [
            {'json': cls.enrollments_json[0], 'status_code': 200},
            {'json': cls.enrollments_json[1], 'status_code': 200},
        ]

        base_edx_url = 'http://edx.example.com'
        cls.enrollment_url = urljoin(base_edx_url, CourseEnrollments.enrollment_url)
        cls.client = EdxApi({'access_token': 'foobar'}, cls.enrollment_url)
        cls.enrollment_client = cls.client.enrollments

    @requests_mock.mock()
    def test_create_enrollment_value(self, mock_req):
        """
        Tests the post request to create an enrollment.
        This just tests that the client expects a JSON object representing the enrollment.
        """
        mock_req.register_uri('POST', self.enrollment_url, self.enrollment_responses)
        course_id = 'dummy_course_id'
        returned_enrollments = [
            self.enrollment_client.create_student_enrollment(course_id),
            self.enrollment_client.create_audit_student_enrollment(course_id),
        ]
        assert [enrollment.json for enrollment in returned_enrollments] == self.enrollments_json

    @requests_mock.mock()
    def test_create_enrollment_body(self, request_mock):
        """
        Tests the post body crafted to create an enrollment.
        """
        request_mock.post(self.enrollment_url, json=self.enrollments_json[0])
        course_id = 'course_id'
        user = 'user'
        enrollment_attributes = {
            'namespace': 'credit',
            'name': 'provider_id',
            'value': 'institution_name',
        }
        self.enrollment_client.create_student_enrollment(
            course_id=course_id,
            mode=ENROLLMENT_MODE_VERIFIED
        )
        self.assertDictEqual(
            request_mock.last_request.json(),
            {
                'course_details': {
                    'course_id': course_id
                },
                'mode': ENROLLMENT_MODE_VERIFIED
            }
        )
        self.enrollment_client.create_audit_student_enrollment(course_id=course_id)
        self.assertDictEqual(
            request_mock.last_request.json(),
            {
                'course_details': {
                    'course_id': course_id
                },
                'mode': ENROLLMENT_MODE_AUDIT
            }
        )
        self.enrollment_client.create_student_enrollment(
            course_id=course_id,
            username=user
        )
        self.assertDictEqual(
            request_mock.last_request.json(),
            {
                'course_details': {
                    'course_id': course_id
                },
                'mode': ENROLLMENT_MODE_AUDIT,
                'user': user
            }
        )
        self.enrollment_client.create_student_enrollment(
            course_id=course_id,
            username=user,
            enrollment_attributes=enrollment_attributes
        )
        self.assertDictEqual(
            request_mock.last_request.json(),
            {
                'enrollment_attributes': enrollment_attributes,
                'course_details': {
                    'course_id': course_id
                },
                'mode': ENROLLMENT_MODE_AUDIT,
                'user': user
            }
        )

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

    @requests_mock.mock()
    def test_deactivate_enrollment(self, request_mock):
        """
        Test that deactivate_enrollment calls the enrollment endpoint with the correct request
        body and returns the deactivated enrollment
        """
        request_mock.post(self.enrollment_url, json=self.enrollments_json[0])
        course_id = 'course_id'
        returned_enrollment = self.enrollment_client.deactivate_enrollment(course_id=course_id)
        self.assertDictEqual(
            request_mock.last_request.json(),
            {
                'course_details': {
                    'course_id': course_id
                },
                'is_active': False
            }
        )
        assert returned_enrollment.json == self.enrollments_json[0]
