"""
Business objects for the Grades API
"""
from collections import Iterable

from six import python_2_unicode_compatible

# pylint: disable=too-few-public-methods


@python_2_unicode_compatible
class CurrentGrades(object):
    """
    Current Grades object representation
    """
    def __init__(self, current_grade_list):
        if not isinstance(current_grade_list, Iterable):
            raise TypeError('CurrentGrades needs a Iterable object')
        self.current_grades = {}
        self.username = None
        for current_grade in current_grade_list:
            if not isinstance(current_grade, CurrentGrade):
                raise ValueError("Only CurrentGrade objects are allowed")
            if self.username is None:
                self.username = current_grade.username
            if self.username is not None and current_grade.username != self.username:
                raise ValueError("Only CurrentGrade objects for the same user are allowed")
            self.current_grades[current_grade.course_id] = current_grade

    def __str__(self):
        return "<Current Grades for user {username}>".format(username=self.username)

    @property
    def all_course_ids(self):
        """Helper property to return all the course ids of the current grades"""
        return self.current_grades.keys()

    @property
    def all_current_grades(self):
        """Helper property to return all the current grade objects"""
        return self.current_grades.values()

    def get_current_grade(self, course_id):
        """Returns the current grade for the given course id"""
        return self.current_grades.get(course_id)


@python_2_unicode_compatible
class CurrentGrade(object):
    """
    Single current grade object representation
    """
    def __init__(self, json):
        self.json = json

    def __str__(self):
        return "<Current Grade for user {user} in course {course}>".format(
            user=self.username,
            course=self.course_id
        )

    @property
    def course_id(self):
        """Shortcut for a nested property"""
        return self.json.get('course_key')

    @property
    def username(self):
        """Returns the username of the user."""
        return self.json.get('username')

    @property
    def passed(self):
        """Whether the user has passed the course"""
        return self.json.get('passed')

    @property
    def percent(self):
        """
        Returns a decimal representation between
        0 and 1 of the student grade for the course
        """
        return self.json.get('percent')

    @property
    def letter_grade(self):
        """
        Returns a letter grade as defined in the
        edX grading_policy (e.g. 'A' 'B' 'C' for 6.002x) or None
        """
        return self.json.get('letter_grade')
