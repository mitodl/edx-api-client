"""Models Tests for the Course List API"""
import json
import os
from unittest import TestCase

from edx_api.course_detail.models import CourseDetail
from .models import Courses


class CoursesTests(TestCase):
    """Tests for courses object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                              'fixtures/course_list.json')) as file_obj:
            cls.courses_json = json.loads(file_obj.read())

        cls.courses = Courses(cls.courses_json)

    def test_str(self):
        """Test the __str__"""
        assert str(self.courses) == "<CourseList>"

    def test_iteration(self):
        """Test iteration through the object"""
        courses_list = list(self.courses)
        assert len(courses_list) == 3

        for course in courses_list:
            assert isinstance(course, CourseDetail)

    def test_get_course_by_id(self):
        """Test retrieving a course by ID"""
        # Test a course that exists
        course = self.courses.courses.get('course-v1:edX+DemoX+Demo_Course')
        assert course is not None
        assert course.course_id == 'course-v1:edX+DemoX+Demo_Course'
        assert course.name == 'Demo Course'

        # Test a course that doesn't exist
        course = self.courses.courses.get('nonexistent-course-id')
        assert course is None

    def test_course_properties(self):
        """Test the properties of a course"""
        course = self.courses.courses.get('course-v1:edX+DemoX+Demo_Course')
        assert course.org == 'edX'
        assert course.number == 'DemoX'
        assert course.name == 'Demo Course'

        assert course.start.year == 2013
        assert course.start.month == 2
        assert course.start.day == 5
