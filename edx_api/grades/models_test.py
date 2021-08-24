"""Models Tests for the Grades API"""

import json
import os.path
from copy import deepcopy
from unittest import TestCase

from .models import (
    CurrentGrade,
    CurrentGradesByCourse,
    CurrentGradesByUser,
)


class CurrentGradesByCourseTests(TestCase):
    """
    Tests for CurrentGradesByCourse
    """
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/course_grades_hawthorn.json')) as file_obj:
            cls.grades_json = json.loads(file_obj.read())

        cls.current_grades = CurrentGradesByCourse(
            [CurrentGrade(json_obj) for json_obj in cls.grades_json]
        )

    def test_expected_iterable(self):
        """CurrentGradesByCourse expects an iterable as input"""
        with self.assertRaises(TypeError):
            CurrentGradesByCourse(123)

    def test_cgbycourse_objects(self):
        """CurrentGradesByCourse can contain only CurrentGrade objects"""
        with self.assertRaises(ValueError):
            CurrentGradesByCourse([{'foo': 'bar'}])

    def test_only_same_course_grades(self):
        """
        CurrentGradesByCourse should only contain grades from a single course_id.
        """
        grades_json = deepcopy(self.grades_json)
        grades_json[0]['course_id'] = "course-v1:A:Nonreal:Course"
        with self.assertRaises(ValueError):
            CurrentGradesByCourse(
                [CurrentGrade(json_obj) for json_obj in grades_json],
            )

    def test_different_usernames(self):
        """Grades can have different users."""
        grades_json = deepcopy(self.grades_json)
        for grade in grades_json:
            grade['course_id'] = grades_json[0]['course_id']
        grades_json[0]['username'] = 'different_username'
        # No exception raised
        CurrentGradesByCourse(
            [CurrentGrade(json_obj) for json_obj in grades_json],
        )

    def test_all_current_grades(self):
        """Test for all_current_grades property"""
        all_grades = self.current_grades.all_current_grades
        assert len(all_grades) == 2
        for grade in all_grades:
            assert isinstance(grade, CurrentGrade)


class CurrentGradesByUserTests(TestCase):
    """
    Tests for CurrentGradesByUser
    """
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/current_grades.json')) as file_obj:
            cls.grades_json = json.loads(file_obj.read())

        cls.current_grades = CurrentGradesByUser(
            [CurrentGrade(json_obj) for json_obj in cls.grades_json]
        )

    def test_expected_iterable(self):
        """CurrentGradesByUser expects an iterable as input"""
        with self.assertRaises(TypeError):
            CurrentGradesByUser(123)

    def test_cgbyuser_objects(self):
        """CurrentGradesByUser can contain only CurrentGrade objects"""
        with self.assertRaises(ValueError):
            CurrentGradesByUser([{'foo': 'bar'}])

    def test_all_course_ids(self):
        """Test for all_course_ids property"""
        assert set(self.current_grades.all_course_ids) == {
            "course-v1:edX+DemoX+Demo_Course", "course-v1:MITx+8.MechCX+2014_T1"
        }

    def test_username_is_different(self):
        """CurrentGradesByUser can contain grades for the user with different username"""
        grades_json = deepcopy(self.grades_json)
        grades_json[0]['username'] = 'other_random_string'
        CurrentGradesByUser([CurrentGrade(json_obj) for json_obj in grades_json])

    def test_get_current_grade(self):
        """Test for get_current_grade method"""
        course_grade = self.current_grades.get_current_grade("course-v1:edX+DemoX+Demo_Course")
        assert isinstance(course_grade, CurrentGrade)
        assert course_grade.course_id == "course-v1:edX+DemoX+Demo_Course"

    def test_all_current_grades(self):
        """Test for all_current_grades property"""
        all_grades = self.current_grades.all_current_grades
        assert len(all_grades) == 2
        for grade in all_grades:
            assert isinstance(grade, CurrentGrade)


class CurrentGradeTests(TestCase):
    """Tests for current grade object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/current_grades.json')) as file_obj:
            cls.grades_json = json.loads(file_obj.read())

        cls.current_grade = CurrentGrade(cls.grades_json[0])

    def test_str(self):
        """Test the __str__"""
        assert str(self.current_grade) == ("<Current Grade for user bob in "
                                           "course course-v1:edX+DemoX+Demo_Course>")

    def test_course_id(self):
        """Test for course_id property"""
        assert self.current_grade.course_id == "course-v1:edX+DemoX+Demo_Course"

    def test_email(self):
        """Test for email property"""
        assert self.current_grade.email == "bob@example.com"

    def test_username(self):
        """Test for user property"""
        assert self.current_grade.username == "bob"

    def test_passed(self):
        """Test for passed property"""
        assert self.current_grade.passed is True

    def test_percent(self):
        """Test for percent property"""
        assert self.current_grade.percent == 0.97

    def test_letter_grade(self):
        """Test for letter_grade property"""
        assert self.current_grade.letter_grade == "Pass"
