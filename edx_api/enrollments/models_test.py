"""Models Tests for the Enrollment API"""

import os.path
import json
from unittest import TestCase

from dateutil import parser

from .models import (
    Enrollments,
    Enrollment,
    CourseDetails,
    CourseMode,
)


class EnrollmentsTests(TestCase):
    """Tests for enrollments object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/user_enrollments.json')) as file_obj:
            cls.enrollments_json = json.loads(file_obj.read())

        cls.enrollments = Enrollments(cls.enrollments_json)

    def test_str(self):
        """Test the __str__"""
        assert str(self.enrollments) == "<Enrollments>"

    def test_enrollments(self):
        """Test the enrolled_courses method"""
        enrollments_list = list(self.enrollments.enrolled_courses)
        assert len(enrollments_list) == 2

        for elem in enrollments_list:
            assert isinstance(elem, Enrollment)

    def test_filter_enrolled_courses(self):
        """Tests helper method"""
        with self.assertRaises(ValueError):
            list(self.enrollments.get_enrolled_courses_by_ids('foo'))

        enrollments_list = list(
            self.enrollments.get_enrolled_courses_by_ids(('course-v1:edX+DemoX+Demo_Course',))
        )
        assert len(enrollments_list) == 1
        assert enrollments_list[0].course_id == 'course-v1:edX+DemoX+Demo_Course'

    def test_get_id_only(self):
        """Test for get_enrolled_course_ids method"""
        enrollments_id_list = list(
            self.enrollments.get_enrolled_course_ids()
        )
        assert len(enrollments_id_list) == 2

        enrollments_id_list = list(
            self.enrollments.get_enrolled_course_ids(('course-v1:edX+DemoX+Demo_Course',))
        )
        assert len(enrollments_id_list) == 1
        assert enrollments_id_list[0] == 'course-v1:edX+DemoX+Demo_Course'

        enrollments_id_list = list(
            self.enrollments.get_enrolled_course_ids(('course-v1:edX+DemoX+Demo_Course', 'foo'))
        )
        assert len(enrollments_id_list) == 1
        assert enrollments_id_list[0] == 'course-v1:edX+DemoX+Demo_Course'

    def test_is_enrolled_in(self):
        """Test for is_enrolled_in"""
        assert self.enrollments.is_enrolled_in('course-v1:foo+bar+baz_course') is False
        assert self.enrollments.is_enrolled_in('course-v1:edX+DemoX+Demo_Course') is True

    def test_get_enrollment_for_course(self):
        """Test for get_enrollment_for_course"""
        assert self.enrollments.get_enrollment_for_course('foo') is None
        enr = self.enrollments.get_enrollment_for_course('course-v1:edX+DemoX+Demo_Course')
        assert isinstance(enr, Enrollment)


class EnrollmentTests(TestCase):
    """Tests for enrollment object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/user_enrollments.json')) as file_obj:
            cls.enrollments_json = json.loads(file_obj.read())

        cls.enrollment_json = cls.enrollments_json[0]
        cls.enrollment = Enrollment(cls.enrollment_json)

    def test_str(self):
        """Test the __str__"""
        assert str(self.enrollment) == ("<Enrollment for user staff in "
                                        "course course-v1:edX+DemoX+Demo_Course>")

    def test_created(self):
        """Test for created property"""
        assert self.enrollment.created == parser.parse("2015-12-22T02:47:17Z")

    def test_mode(self):
        """Test for mode property"""
        assert self.enrollment.mode == "honor"

    def test_is_active(self):
        """Test for is_active property"""
        assert self.enrollment.is_active is True

    def test_course_details(self):
        """Test for course_details property"""
        assert isinstance(self.enrollment.course_details, CourseDetails)

    def test_user(self):
        """Test for user property"""
        assert self.enrollment.user == "staff"

    def test_course_id(self):
        """Test for course id property"""
        assert self.enrollment.course_id == "course-v1:edX+DemoX+Demo_Course"
        assert self.enrollment.course_id == self.enrollment.course_details.course_id

    def test_is_verified(self):
        """Test for is_active property"""
        assert self.enrollment.is_verified is False


class CourseDetailsTests(TestCase):
    """Tests for course details object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/user_enrollments.json')) as file_obj:
            cls.enrollments_json = json.loads(file_obj.read())

        cls.course_details_json = cls.enrollments_json[0]['course_details']
        cls.course_details = CourseDetails(cls.course_details_json)

    def test_str(self):
        """Test the __str__"""
        assert str(self.course_details) == ("<Enrollment details for course "
                                            "course-v1:edX+DemoX+Demo_Course>")

    def test_course_id(self):
        """Test for course_id property"""
        assert self.course_details.course_id == "course-v1:edX+DemoX+Demo_Course"

    def test_course_start(self):
        """Test for course_start property"""
        assert self.course_details.course_start == parser.parse("2013-02-05T05:00:00Z")

    def test_course_end(self):
        """Test for course_end property"""
        assert self.course_details.course_end == parser.parse("2015-05-10T23:59:00Z")

    def test_enrollment_start(self):
        """Test for enrollment_start property"""
        assert self.course_details.enrollment_start == parser.parse("2013-02-05T05:00:01Z")

    def test_enrollment_end(self):
        """Test for enrollment_end property"""
        assert self.course_details.enrollment_end == parser.parse("2015-05-10T23:58:00Z")

    def test_invite_only(self):
        """Test for invite_only property"""
        assert self.course_details.invite_only is False

    def test_course_modes(self):
        """Test for course_modes property"""
        course_modes_list = list(self.course_details.course_modes)
        assert len(course_modes_list) == 1
        for elem in course_modes_list:
            assert isinstance(elem, CourseMode)


class CourseModeTests(TestCase):
    """Tests for course mode object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/user_enrollments.json')) as file_obj:
            cls.enrollments_json = json.loads(file_obj.read())

        cls.course_mode_json = cls.enrollments_json[0]['course_details']['course_modes'][0]
        cls.course_mode = CourseMode(cls.course_mode_json)

    def test_currency(self):
        """Test for currency property"""
        assert self.course_mode.currency == "usd"

    def test_description(self):
        """Test for description property"""
        assert self.course_mode.description is None

    def test_expiration_datetime(self):
        """Test for expiration_datetime property"""
        assert self.course_mode.expiration_datetime is None

    def test_min_price(self):
        """Test for min_price property"""
        assert self.course_mode.min_price == 0

    def test_name(self):
        """Test for name property"""
        assert self.course_mode.name == "Audit"

    def test_slug(self):
        """Test for slug property"""
        assert self.course_mode.slug == "audit"

    def test_suggested_prices(self):
        """Test for  property"""
        assert self.course_mode.suggested_prices == ""
