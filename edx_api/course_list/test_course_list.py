"""Tests for Course List API"""

import json
import os.path
from unittest import TestCase
from unittest.mock import Mock

from edx_api.course_list import CourseList
from edx_api.course_detail.models import CourseDetail


class CourseListTests(TestCase):
    """Tests for CourseList class"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.base_url = "http://192.168.33.10:8000/"
        fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")

        with open(os.path.join(fixtures_dir, "course_list_response.json")) as f:
            cls.course_list_response = json.load(f)

        with open(os.path.join(fixtures_dir, "course_list_page1.json")) as f:
            cls.course_list_page1 = json.load(f)

        with open(os.path.join(fixtures_dir, "course_list_page2.json")) as f:
            cls.course_list_page2 = json.load(f)

        with open(os.path.join(fixtures_dir, "course_list_empty.json")) as f:
            cls.course_list_empty = json.load(f)

    def setUp(self):
        """Set up each test"""
        self.requester = Mock()
        self.course_list = CourseList(self.requester, self.base_url)

    def test_init(self):
        """Test CourseList initialization"""
        course_list = CourseList(self.requester, self.base_url)
        self.assertEqual(course_list._requester, self.requester)
        self.assertEqual(course_list._base_url, self.base_url)
        self.assertEqual(course_list.course_list_url, '/api/courses/v1/courses/')

    def test_get_courses_basic(self):
        """Test basic get_courses without parameters"""
        mock_response = Mock()
        mock_response.json.return_value = self.course_list_response
        self.requester.get.return_value = mock_response

        courses = list(self.course_list.get_courses())

        self.requester.get.assert_called_once()
        call_args = self.requester.get.call_args
        self.assertIn('/api/courses/v1/courses/', call_args[0][0])

        params = call_args[1]['params']
        self.assertEqual(params['page_size'], 100)
        self.assertNotIn('org', params)
        self.assertNotIn('search_term', params)
        self.assertNotIn('username', params)
        self.assertNotIn('active_only', params)

        self.assertEqual(len(courses), 2)
        self.assertIsInstance(courses[0], CourseDetail)
        self.assertEqual(courses[0].course_id, "course-v1:edX+DemoX+Demo_Course")
        self.assertEqual(courses[1].course_id, "course-v1:MITx+6.00.1x+3T2015")

    def test_get_courses_with_filters(self):
        """Test get_courses with various filter parameter combinations"""
        test_cases = [
            {
                'name': 'valid_filters',
                'params': {'org': 'MIT', 'search_term': 'python', 'username': 'testuser', 'active_only': True},
                'should_contain': ['org', 'search_term', 'username', 'active_only']
            },
            {
                'name': 'falsy_values',
                'params': {'org': '', 'search_term': None, 'username': '', 'active_only': None},
                'should_not_contain': ['org', 'search_term', 'username', 'active_only']
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case['name']):
                mock_response = Mock()
                mock_response.json.return_value = self.course_list_response
                self.requester.get.return_value = mock_response

                courses = list(self.course_list.get_courses(**test_case['params']))

                call_args = self.requester.get.call_args
                params = call_args[1]['params']

                if 'should_contain' in test_case:
                    for param in test_case['should_contain']:
                        self.assertIn(param, params)
                        self.assertEqual(params[param], test_case['params'][param])

                if 'should_not_contain' in test_case:
                    for param in test_case['should_not_contain']:
                        self.assertNotIn(param, params)

        self.assertEqual(len(courses), 2)

    def test_get_courses_with_course_keys(self):
        """Test get_courses with course_keys"""
        mock_response = Mock()
        mock_response.json.return_value = self.course_list_response
        self.requester.get.return_value = mock_response

        course_keys = ['course-v1:edX+DemoX+Demo_Course', 'course-v1:MITx+6.00.1x+3T2015']

        courses = list(self.course_list.get_courses(course_keys=course_keys))

        call_args = self.requester.get.call_args
        params = call_args[1]['params']
        self.assertEqual(params['course_keys'], course_keys)

        self.assertEqual(len(courses), 2)

    def test_get_courses_pagination(self):
        """Test get_courses with pagination"""
        mock_response1 = Mock()
        mock_response1.json.return_value = self.course_list_page1

        mock_response2 = Mock()
        mock_response2.json.return_value = self.course_list_page2

        self.requester.get.side_effect = [mock_response1, mock_response2]
        courses = list(self.course_list.get_courses())

        self.assertEqual(self.requester.get.call_count, 2)

        call_args1 = self.requester.get.call_args_list[0]
        params1 = call_args1[1]['params']
        self.assertEqual(params1['page'], 1)

        call_args2 = self.requester.get.call_args_list[1]
        params2 = call_args2[1]['params']
        self.assertEqual(params2['page'], 2)

        self.assertEqual(len(courses), 2)

    def test_get_courses_with_large_course_keys_batching(self):
        """Test that large course_keys lists are properly batched"""
        mock_response = Mock()
        mock_response.json.return_value = self.course_list_response
        self.requester.get.return_value = mock_response

        course_keys = [f'course-v1:Test+Course{i}+2024' for i in range(250)]
        courses = list(self.course_list.get_courses(course_keys=course_keys))

        self.assertEqual(self.requester.get.call_count, 3)

        call_args_list = self.requester.get.call_args_list

        params1 = call_args_list[0][1]['params']
        self.assertEqual(len(params1['course_keys']), 100)

        params2 = call_args_list[1][1]['params']
        self.assertEqual(len(params2['course_keys']), 100)

        params3 = call_args_list[2][1]['params']
        self.assertEqual(len(params3['course_keys']), 50)

        self.assertEqual(len(courses), 6)

    def test_get_courses_http_error(self):
        """Test get_courses handles HTTP errors"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        self.requester.get.return_value = mock_response

        with self.assertRaises(Exception):
            list(self.course_list.get_courses())

    def test_get_courses_empty_response(self):
        """Test get_courses with empty response"""
        mock_response = Mock()
        mock_response.json.return_value = self.course_list_empty
        self.requester.get.return_value = mock_response

        courses = list(self.course_list.get_courses())
        self.assertEqual(len(courses), 0)
