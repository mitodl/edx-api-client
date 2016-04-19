"""Models Tests for the Course Detail API"""

import os.path
import json
from unittest import TestCase

from dateutil import parser

from .models import (
    CourseDetail,
    Media,
)


class CourseDetailTests(TestCase):
    """Tests for course detail object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/course_detail.json')) as file_obj:
            cls.detail_json = json.loads(file_obj.read())

        cls.detail = CourseDetail(cls.detail_json)

    def test_str(self):
        """Test the __str__"""
        assert str(self.detail) == "<Course detail for course-v1:edX+DemoX+Demo_Course>"

    def test_repr(self):
        """Test the __repr__"""
        assert self.detail.__repr__() == "<Course detail for course-v1:edX+DemoX+Demo_Course>"

    def test_blocks_url(self):
        """Test for blocks_url property"""
        assert self.detail.blocks_url == ("http://192.168.33.10:8000/api/courses/v1/blocks/"
                                          "?course_id=course-v1%3AedX%2BDemoX%2BDemo_Course")

    def test_effort(self):
        """Test for effort property"""
        assert self.detail.effort == "7 hours"

    def test_end(self):
        """Test for end property"""
        assert self.detail.end == parser.parse("2016-09-01T05:00:00Z")

    def test_enrollment_start(self):
        """Test for enrollment_start property"""
        assert self.detail.enrollment_start == parser.parse("2016-03-01T00:00:00Z")

    def test_enrollment_end(self):
        """Test for enrollment_end property"""
        assert self.detail.enrollment_end is None

    def test_course_id(self):
        """Test for course_id property"""
        assert self.detail.course_id == "course-v1:edX+DemoX+Demo_Course"

    def test_name(self):
        """Test for name property"""
        assert self.detail.name == "edX Demonstration Course"

    def test_number(self):
        """Test for number property"""
        assert self.detail.number == "DemoX"

    def test_org(self):
        """Test for org property"""
        assert self.detail.org == "edX"

    def test_short_description(self):
        """Test for short_description property"""
        assert self.detail.short_description == ""

    def test_start(self):
        """Test for start property"""
        assert self.detail.start == parser.parse("2016-03-25T05:00:00Z")

    def test_start_display(self):
        """Test for start_display property"""
        assert self.detail.start_display == "March 25, 2016"

    def test_start_type(self):
        """Test for start_type property"""
        assert self.detail.start_type == "timestamp"

    def test_overview(self):
        """Test for overview property"""
        assert self.detail.overview == ("<h2>About This Course</h2>\n   <p>Include your long course"
                                        " description here. The long course description should "
                                        "contain 150-400 words.</p>\n")

    def test_media(self):
        """Test for media property"""
        list_media = list(self.detail.media)
        assert len(list_media) == 2
        assert Media(
            type="course_image",
            url="/asset-v1:edX+DemoX+Demo_Course+type@asset+block@images_course_image.jpg"
        ) in list_media
        assert Media(type="course_video", url=None) in list_media
