"""Models Tests for the Course Runs API models"""

import json
import os.path
from unittest import TestCase

from dateutil import parser

from .models import CourseRun, CourseRunList


class CourseRunTests(TestCase):
    """Tests for course run object"""

    @classmethod
    def setUpClass(cls):
        with open(
            os.path.join(os.path.dirname(__file__), "fixtures/course_run.json")
        ) as file_obj:
            cls.detail_json = json.loads(file_obj.read())

        cls.detail = CourseRun(cls.detail_json)

    def test_str(self):
        """Test the __str__"""
        assert str(self.detail) == "<Course run details for course-v1:ORG+NUMBER+RUN>"

    def test_repr(self):
        """Test the __repr__"""
        assert (
            self.detail.__repr__()
            == "<Course run details for course-v1:ORG+NUMBER+RUN>"
        )

    def test_schedule(self):
        """Test for schedule property"""
        assert self.detail.schedule == {
            "start": "2025-01-01T00:00:00Z",
            "end": "2030-01-01T00:05:00Z",
            "enrollment_start": "2025-01-02T00:00:00Z",
            "enrollment_end": None,
        }

    def test_start(self):
        """Test for start property"""
        assert self.detail.start == parser.parse("2025-01-01T00:00:00Z")

    def test_end(self):
        """Test for end property"""
        assert self.detail.end == parser.parse("2030-01-01T00:05:00Z")

    def test_enrollment_start(self):
        """Test for enrollment_start property"""
        assert self.detail.enrollment_start == parser.parse("2025-01-02T00:00:00Z")

    def test_enrollment_end(self):
        """Test for enrollment_end property"""
        assert self.detail.enrollment_end is None

    def test_pacing_type(self):
        """Test for pacing_type property"""
        assert self.detail.pacing_type == "instructor_paced"

    def test_course_id(self):
        """Test for course_id property"""
        assert self.detail.course_id == "course-v1:ORG+NUMBER+RUN"

    def test_title(self):
        """Test for title property"""
        assert self.detail.title == "Test Course"

    def test_card_image(self):
        """Test for card_image property"""
        assert self.detail.card_image == (
            "http://studio.local.openedx.io:8001/asset-v1:ORG+NUMBER+RUN+type@asset+block@images_course_image.jpg"
        )

    def test_org(self):
        """Test for org property"""
        assert self.detail.org == "ORG"

    def test_number(self):
        """Test for number property"""
        assert self.detail.number == "NUMBER"

    def test_run(self):
        """Test for run property"""
        assert self.detail.run == "RUN"


class CourseRunListTests(TestCase):
    """Tests for course run list object"""

    @classmethod
    def setUpClass(cls):
        with open(
            os.path.join(os.path.dirname(__file__), "fixtures/course_run_list.json")
        ) as file_obj:
            cls.detail_json = json.loads(file_obj.read())

        cls.list_detail = CourseRunList(cls.detail_json)

    def test_next(self):
        """Test for next property"""
        assert self.list_detail.next == (
            "http://studio.local.openedx.io:8001/api/v1/course_runs/?page=2"
        )

    def test_previous(self):
        """Test for previous property"""
        assert self.list_detail.previous == None

    def test_count(self):
        """Test for count property"""
        assert self.list_detail.count == 10

    def test_num_pages(self):
        """Test for num_pages property"""
        assert self.list_detail.num_pages == 5

    def test_current_page(self):
        """Test for current_page property"""
        assert self.list_detail.current_page == 1

    def test_start(self):
        """Test for start property"""
        assert self.list_detail.start == 0

    def test_results(self):
        """Test for results property"""
        assert len(self.list_detail.results) == 2
        assert isinstance(self.list_detail.results[0], CourseRun)
        assert isinstance(self.list_detail.results[1], CourseRun)
