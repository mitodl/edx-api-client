"""
Integration tests.

Thes run against actual edx apis.

NOTE: To run this test you need a running instance of edX properly configured.
This means that you need:
- the edx demo course
- the user staff being "staff" of such course
- the course being open to enrollment
- the course having the ccx enabled in the advanced settings
- a valid access token for the user "staff"
- you run the following code in a python shell inside your devstack
  instance to create a certificate:
```
from certificates.models import CertificateStatuses
from django.contrib.auth.models import User
from certificates.tests.factories import GeneratedCertificateFactory
from opaque_keys.edx.keys import CourseKey
course_key = CourseKey.from_string('course-v1:edX+DemoX+Demo_Course')
staff = User.objects.get(username='staff')
GeneratedCertificateFactory.create(
    user=staff,
    course_id=course_key,
    status=CertificateStatuses.downloadable,
    mode='verified',
    download_url='www.google.com', grade="0.88",
)
```
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


@require_integration_settings
def test_get_certificate():
    """
    Gets the certificate for the demo course.
    See this module docstring for the code to run to create one
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    certificate = api.certificates.get_student_certificate(
        'staff', 'course-v1:edX+DemoX+Demo_Course')
    assert certificate.username == 'staff'
    assert certificate.is_verified is True

    certificates = api.certificates.get_student_certificates('staff')
    assert len(certificates.all_courses_certs) >= 1
    assert 'course-v1:edX+DemoX+Demo_Course' in certificates.all_courses_certs
    assert 'course-v1:edX+DemoX+Demo_Course' in certificates.all_courses_verified_certs
