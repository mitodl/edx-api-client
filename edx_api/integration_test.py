"""
Integration tests.

Thes run against actual edx apis.

NOTE: To run this test you need a running instance of edX properly configured.
This means that you need:
- the edx demo course
- the user staff being "staff" of such course
- the course being open to enrollment
- a valid access token for the user "staff"
"""
import os

import pytest
from six.moves.urllib.parse import urljoin  # pylint: disable=import-error

from .client import EdxApi


ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000/')

# pylint: disable=invalid-name
require_integration_settings = pytest.mark.skipif(
    not ACCESS_TOKEN or not BASE_URL,
    reason="You must specify the credential env vars"
)


@require_integration_settings
def test_course_structure():
    """
    Pull down the course structure and validate it has the correct entries.
    This test assumes that the used user can access the course.
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    structure = api.course_structure.course_blocks('course-v1:edX+DemoX+Demo_Course', 'staff')

    titles = [
        block.title for block in structure.root.children
        if block.visible
    ]

    assert titles == [
        'Introduction',
        'Example Week 1: Getting Started',
        'Example Week 2: Get Interactive',
        'Example Week 3: Be Social',
        'About Exams and Certificates',
        'holding section',
    ]


@require_integration_settings
def test_enrollments():
    """
    Enrolls the user in a course and then pulls down the enrollments for the user.
    This assumes that the course in the edX instance is available for enrollment.
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)

    # the enrollment will be done manually until
    # a client to enroll the student is implemented
    requester = api.get_requester()
    requester.post(
        urljoin(BASE_URL, '/api/enrollment/v1/enrollment'),
        json={"course_details": {"course_id": 'course-v1:edX+DemoX+Demo_Course'}}
    )

    enrollments = api.enrollments.get_student_enrollments()

    enrolled_courses = [
        enrolled_course.course_details.course_id
        for enrolled_course in enrollments.enrolled_courses
    ]

    assert 'course-v1:edX+DemoX+Demo_Course' in enrolled_courses


@require_integration_settings
def test_course_details():
    """
    Pull down the course details.
    This test assumes that the used user is not anonymous.
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    details = api.course_detail.get_detail('course-v1:edX+DemoX+Demo_Course')

    assert details.course_id == "course-v1:edX+DemoX+Demo_Course"
    assert details.name == "edX Demonstration Course"


@require_integration_settings
def test_create_ccx():
    """
    Creates a CCX for the demo course. This course *MUST* have ccx enabled in
    the advanced settings.
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    ccx_id = api.ccx.create(
        'course-v1:edX+DemoX+Demo_Course',
        'verified@example.com',
        100,
        'My CCX from test_create_ccx integration test via edx-api-client.'
    )

    assert ccx_id is not None
    assert '@' in ccx_id  # follows ccx format
