"""
Integration tests.

These run against actual edX APIs.

NOTE: To run this test you need a running instance of edX properly configured.
This means that you need:
- the edx demo course set to course mode 'audit' (the default)
- the user staff being "staff" of such course
- the course being open to enrollment
- the course having the ccx enabled in the advanced settings
- a valid access token for the user "staff"
- another course is available with enrollment open and "staff" NOT enrolled
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

from mock import patch
import pytest
from requests.exceptions import HTTPError
from requests import Response
from six.moves.urllib.parse import urljoin  # pylint: disable=import-error

from .client import EdxApi


ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000/')
ENROLLMENT_CREATION_COURSE_ID = os.getenv('ENROLLMENT_CREATION_COURSE_ID')

# pylint: disable=invalid-name
require_integration_settings = pytest.mark.skipif(
    not ACCESS_TOKEN or not BASE_URL,
    reason="You must specify the credential env vars"
)

require_integration_settings_course_id = pytest.mark.skipif(
    not ACCESS_TOKEN or not BASE_URL or not ENROLLMENT_CREATION_COURSE_ID,
    reason="You must specify the credential env vars and the alternate course id for enrollments"
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


@require_integration_settings_course_id
def test_create_enrollment():
    """
    Integration test to enroll the user in a course
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    enrollment = api.enrollments.create_audit_student_enrollment(ENROLLMENT_CREATION_COURSE_ID)
    assert enrollment.course_id == ENROLLMENT_CREATION_COURSE_ID


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


class FakeErroredResponse(object):
    """Fake requests response"""
    def __init__(self, status_code):
        """
        Build a fake error response
        """
        self.error = HTTPError(response=Response())
        self.error.response = Response()
        self.error.response.status_code = status_code

    def raise_for_status(self):
        """Raise an HTTPError"""
        raise self.error


@require_integration_settings
def test_get_certificate_500_error():
    """
    Asserts that a 500 error returned from EDX will be propagated
    """

    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    username = 'staff'
    course_key = 'course-v1:edX+DemoX+Demo_Course'

    certificates = api.certificates
    old_requester_get = certificates.requester.get

    def mocked_get(url, *args, **kwargs):
        """
        Return an error for specific URLs
        """
        if '/api/certificates/v0/certificates/' in url:
            return FakeErroredResponse(status_code=500)
        return old_requester_get(url, *args, **kwargs)

    with patch.object(certificates.requester, 'get', autospec=True) as get:
        get.side_effect = mocked_get
        with pytest.raises(HTTPError):
            certificates.get_student_certificate(
                username, course_key
            )

        with pytest.raises(HTTPError):
            certificates.get_student_certificates(username)


@require_integration_settings
def test_get_certificate_404_error():
    """
    Asserts that a 404 returned from EDX will be silenced for get_student_certificates
    """

    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    username = 'staff'
    course_key = 'course-v1:edX+DemoX+Demo_Course'

    certificates = api.certificates
    old_requester_get = certificates.requester.get

    def mocked_get(url, *args, **kwargs):
        """
        Return an error for specific URLs
        """
        if '/api/certificates/v0/certificates/' in url:
            return FakeErroredResponse(status_code=404)
        return old_requester_get(url, *args, **kwargs)

    with patch.object(certificates.requester, 'get', autospec=True) as get:
        get.side_effect = mocked_get
        with pytest.raises(HTTPError):
            certificates.get_student_certificate(
                username, course_key
            )

        # Note no error here, just empty list
        certs = certificates.get_student_certificates(username)
        assert not certs.all_courses_certs


@require_integration_settings
def test_get_current_grade():
    """
    Gets the user current grade.
    If an user is enrolled in a course she has a current grade (probably with percent == 0.0)
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    course_grade = api.current_grades.get_student_current_grade(
        'staff', 'course-v1:edX+DemoX+Demo_Course')
    assert course_grade.username == 'staff'

    course_grades = api.current_grades.get_student_current_grades('staff')
    assert len(course_grades.all_course_ids) >= 1
    assert 'course-v1:edX+DemoX+Demo_Course' in course_grades.all_course_ids


@require_integration_settings
def test_user_info():
    """
    Gets information about the logged in user
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    info = api.user_info.get_user_info()
    assert info.username == 'staff'
    assert info.name == ''
    assert info.email == 'staff@example.com'
    assert isinstance(info.user_id, int)
