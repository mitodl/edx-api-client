"""Models Tests for the Grades API"""

import json
import os.path
from copy import deepcopy
from unittest import TestCase

from .models import (
    CurrentGrade,
    CurrentGrades,
)


class CurrentGradesTests(TestCase):
    """Tests for current grades object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/current_grades.json')) as file_obj:
            cls.grades_json = json.loads(file_obj.read())

        cls.current_grades = CurrentGrades([CurrentGrade(json_obj) for json_obj in cls.grades_json])

    def test_str(self):
        """Test the __str__"""
        assert str(self.current_grades) == "<Current Grades for user bob>"

    def test_expected_iterable(self):
        """CurrentGrades expects an iterable as input"""
        with self.assertRaises(TypeError):
            CurrentGrades(123)

    def test_only_same_user_grades(self):
        """CurrentGrades can contain only grades for the same user"""
        grades_json = deepcopy(self.grades_json)
        grades_json[0]['username'] = 'other_random_string'
        with self.assertRaises(ValueError):
            CurrentGrades([CurrentGrade(json_obj) for json_obj in grades_json])

    def test_currentgrade_objects(self):
        """CurrentGrades can contain only CurrentGrade objects"""
        with self.assertRaises(ValueError):
            CurrentGrades([{'foo': 'bar'}])

    def test_all_course_ids(self):
        """Test for all_course_ids property"""
        assert sorted(list(self.current_grades.all_course_ids)) == sorted(
            ["course-v1:edX+DemoX+Demo_Course", "course-v1:MITx+8.MechCX+2014_T1"])

    def test_all_current_grades(self):
        """Test for all_current_grades property"""
        all_grades = self.current_grades.all_current_grades
        assert len(all_grades) == 2
        for grade in all_grades:
            assert isinstance(grade, CurrentGrade)

    def test_get_current_grade(self):
        """Test for get_current_grade method"""
        course_grade = self.current_grades.get_current_grade("course-v1:edX+DemoX+Demo_Course")
        assert isinstance(course_grade, CurrentGrade)
        assert course_grade.course_id == "course-v1:edX+DemoX+Demo_Course"


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
