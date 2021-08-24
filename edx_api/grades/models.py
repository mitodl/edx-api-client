"""
Business objects for the Grades API
"""
from collections.abc import Iterable
# pylint: disable=too-few-public-methods


class CurrentGrades(object):
    """
    Current Grades object representation
    """
    def __init__(self, current_grade_list):
        if not isinstance(current_grade_list, Iterable):
            raise TypeError('CurrentGrades needs an Iterable object')

    @property
    def all_current_grades(self):
        """Helper property to return all the CurrentGrade objects"""
        return self.current_grades.values()  # pylint: disable=no-member


class CurrentGradesByCourse(CurrentGrades):
    """
    Represents the current grades for a specific course
    """
    def __init__(self, current_grade_list):
        """
        Args:
            current_grade_list (list): A list of the CurrentGrade objects
        """
        super(CurrentGradesByCourse, self).__init__(current_grade_list)
        self.course_id = None
        self.current_grades = {}
        for current_grade in current_grade_list:
            if not isinstance(current_grade, CurrentGrade):
                raise ValueError("Only CurrentGrade objects are allowed")
            if self.course_id is None:
                self.course_id = current_grade.course_id
            if self.course_id is not None and current_grade.course_id != self.course_id:
                raise ValueError("Only CurrentGrade objects for the same course are allowed")
            self.current_grades[current_grade.username] = current_grade

    def __str__(self):
        return "<Current Grades for course {course_id}>".format(
            course_id=self.course_id
        )

    @property
    def all_usernames(self):
        """Helper property to return all the usernames of the current grades"""
        return self.current_grades.keys()


class CurrentGradesByUser(CurrentGrades):
    """
    Represents the current grades for a specific user
    """
    def __init__(self, current_grade_list):
        """
        Args:
            current_grade_list (list): A list of the CurrentGrade objects
        """
        super(CurrentGradesByUser, self).__init__(current_grade_list)
        self.username = None
        self.current_grades = {}
        for current_grade in current_grade_list:
            if not isinstance(current_grade, CurrentGrade):
                raise ValueError("Only CurrentGrade objects are allowed")
            self.current_grades[current_grade.course_id] = current_grade

    def __str__(self):
        return "<Current Grades for user {username}>".format(
            username=self.username
        )

    @property
    def all_course_ids(self):
        """Helper property to return all the course ids of the current grades"""
        return self.current_grades.keys()

    def get_current_grade(self, course_id):
        """Returns the current grade for the given course id"""
        return self.current_grades.get(course_id)


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
        return self.json.get('course_id')

    @property
    def email(self):
        """Returns email of the user"""
        return self.json.get('email')

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
