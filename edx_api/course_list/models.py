"""
Business objects for the course list API
"""
from ..course_detail.models import CourseDetail


class Courses:
    """
    Container for course list results
    """

    def __init__(self, payload):
        self.courses = {}
        for course_json in payload:
            course = CourseDetail(course_json)
            self.courses[course.course_id] = course

    def __str__(self):
        return "<CourseList>"

    def __iter__(self):
        for course in self.courses.values():
            yield course

    def __len__(self):
        return len(self.courses)
