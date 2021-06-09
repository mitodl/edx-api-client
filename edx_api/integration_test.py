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
- the user staff is enrolled in, at least, two courses
- make sure LMS's settings.EDX_API_TOKEN value is the same as the token used here
- make sure user staff is admin in the demo course
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
from requests import Response, Timeout
from urllib.parse import urljoin

from edx_api.constants import ENROLLMENT_MODE_AUDIT, ENROLLMENT_MODE_VERIFIED
from edx_api.client import EdxApi


ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL', 'http://localhost:18000/')
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


class FakeTimeoutResponse(object):
    """Fake requests response"""
    def __init__(self, status_code):
        """
        Build a fake error response
        """
        self.error = Timeout(response=Response())
        self.error.response = Response()
        self.error.response.status_code = status_code

    def raise_for_status(self):
        """Raise an HTTPError"""
        raise self.error

    @staticmethod
    def json():
        """dummy error json"""
        return {
            "message": "time out"
        }


def mocked_timeout(url, *args, **kwargs):  # pylint: disable=unused-argument
    """
    Return a time out error.
    """
    return FakeTimeoutResponse(status_code=408)


@require_integration_settings
def test_course_structure():
    """
    Pull down the course structure and validate it has the correct entries.
    This test assumes that the used user can access the course.
    """
    api = EdxApi({'access_token': ACCESS_TOKEN, 'api_key': API_KEY}, base_url=BASE_URL)
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
    api = EdxApi({'access_token': ACCESS_TOKEN, 'api_key': API_KEY}, base_url=BASE_URL)

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
def test_create_verified_enrollment():
    """
    Integration test to enroll the user in a course with `verified` mode
    """
    api = EdxApi({'access_token': ACCESS_TOKEN, 'api_key': API_KEY}, base_url=BASE_URL)
    enrollment = api.enrollments.create_student_enrollment(
        course_id=ENROLLMENT_CREATION_COURSE_ID,
        mode=ENROLLMENT_MODE_VERIFIED,
        username="staff"
    )
    assert enrollment.course_id == ENROLLMENT_CREATION_COURSE_ID
    assert enrollment.mode == ENROLLMENT_MODE_VERIFIED


@require_integration_settings_course_id
def test_create_audit_enrollment():
    """
    Integration test to enroll the user in a course with `audit` mode
    """
    api = EdxApi({'access_token': ACCESS_TOKEN, 'api_key': API_KEY}, base_url=BASE_URL)
    enrollment = api.enrollments.create_student_enrollment(
        course_id=ENROLLMENT_CREATION_COURSE_ID,
        mode=ENROLLMENT_MODE_AUDIT,
        username="staff"
    )
    assert enrollment.course_id == ENROLLMENT_CREATION_COURSE_ID
    assert enrollment.mode == ENROLLMENT_MODE_AUDIT


@require_integration_settings_course_id
def test_deactivate_enrollment():
    """
    Integration test to enroll then deactivate a user in a course
    """
    api = EdxApi({'access_token': ACCESS_TOKEN, 'api_key': API_KEY}, base_url=BASE_URL)
    api.enrollments.create_student_enrollment(
        course_id=ENROLLMENT_CREATION_COURSE_ID,
        mode=ENROLLMENT_MODE_AUDIT
    )
    deactivated_enrollment = api.enrollments.deactivate_enrollment(
        course_id=ENROLLMENT_CREATION_COURSE_ID
    )
    assert deactivated_enrollment.course_id == ENROLLMENT_CREATION_COURSE_ID
    assert deactivated_enrollment.is_active is False


@require_integration_settings_course_id
def test_create_enrollment_timeout():
    """
     Asserts request timeout error on enrollment api
    """
    api = EdxApi({'access_token': ACCESS_TOKEN, 'api_key': API_KEY}, base_url=BASE_URL)
    enrollments = api.enrollments
    with patch.object(enrollments.requester, 'post', autospec=True) as post:
        post.side_effect = mocked_timeout
        with pytest.raises(Timeout):
            enrollments.create_student_enrollment(ENROLLMENT_CREATION_COURSE_ID)


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
def test_course_details_timeout():
    """
    assert timeout exception on get course_detail
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    course_detail = api.course_detail

    with patch.object(course_detail._requester, 'get', autospec=True) as get:   # pylint: disable=protected-access
        get.side_effect = mocked_timeout
        with pytest.raises(Timeout):
            course_detail.get_detail('course-v1:edX+DemoX+Demo_Course')


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
def test_get_timeout_error_ccx():
    """
    Asserts request timeout error on ccx
    """

    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    ccx = api.ccx

    with patch.object(ccx.requester, 'post', autospec=True) as post:
        post.side_effect = mocked_timeout
        with pytest.raises(Timeout):
            ccx.create(
                'course-v1:edX+DemoX+Demo_Course',
                'verified@example.com',
                100,
                'My CCX from test_create_ccx integration test via edx-api-client.'
            )


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
def test_get_certificate_timeout_error():
    """
    Asserts request timeout error on certificate apis
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    username = 'staff'
    course_key = 'course-v1:edX+DemoX+Demo_Course'
    certificates = api.certificates

    with patch.object(certificates.requester, 'get', autospec=True) as get:
        get.side_effect = mocked_timeout
        with pytest.raises(Timeout):
            certificates.get_student_certificate(
                username, course_key
            )

        with pytest.raises(Timeout):
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

    student_grades = api.current_grades.get_student_current_grades('staff')
    assert len(student_grades.all_course_ids) >= 1
    assert 'course-v1:edX+DemoX+Demo_Course' in student_grades.all_course_ids

    course_grades = api.current_grades.get_course_current_grades('course-v1:edX+DemoX+Demo_Course')
    assert len(course_grades.all_usernames) >= 1
    assert 'honor' in course_grades.all_usernames


@require_integration_settings
def test_get_current_grade_timeout():
    """
    assert timeout exception on get current grade.
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    current_grades = api.current_grades
    with patch.object(current_grades.requester, 'get', autospec=True) as get:
        get.side_effect = mocked_timeout
        with pytest.raises(Timeout):
            current_grades.get_student_current_grade('staff', 'course-v1:edX+DemoX+Demo_Course')


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


@require_integration_settings
def test_user_info_timeout():
    """
    assert timeout exception on user_info
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    user_info = api.user_info
    with patch.object(user_info.requester, 'get', autospec=True) as get:
        get.side_effect = mocked_timeout
        with pytest.raises(Timeout):
            user_info.get_user_info()


@require_integration_settings
def test_enrollments_list():
    """
    Enrolls the user in a course and then pulls down the enrollments for the user.
    This assumes that the course in the edX instance is available for enrollment.
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    enrollments = api.enrollments.get_enrollments()

    cnt = 0
    for enrollment in enrollments:
        assert enrollment.course_id
        assert enrollment.created
        assert enrollment.mode
        assert enrollment.is_active
        assert enrollment.user
        if enrollment.mode != ENROLLMENT_MODE_VERIFIED:
            assert not enrollment.is_verified
        else:
            assert enrollment.is_verified
        cnt += 1

    assert cnt >= 2


@require_integration_settings
def test_user_name_update():
    """
    Asserts that update user's name api updates the full name of the user correctly.
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    user_name = 'Test Name'
    updated_user = api.user_info.update_user_name('staff', user_name)
    assert updated_user.username == 'staff'
    assert updated_user.name == user_name
