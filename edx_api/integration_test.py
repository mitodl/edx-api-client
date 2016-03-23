"""
Integration tests.

Thes run against actual edx apis.
"""
import os
import pytest
from .client import EdxApi


ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000/')

# pylint: disable=invalid-name
require_integration_settings = pytest.mark.skipif(
    not ACCESS_TOKEN or not BASE_URL,
    reason="You must specify the credential env vars"
)


@require_integration_settings
def test_course_structure():
    """
    Pull down the course structure and validate it has the correct entries.
    """
    api = EdxApi({'access_token': ACCESS_TOKEN}, base_url=BASE_URL)
    structure = api.course_structure.course_blocks(
        'course-v1:edX+DemoX+Demo_Course',
        'staff'
    )

    titles = [
        block.title for block in structure.root.children
        if block.visible
    ]

    assert titles == [
        'Introduction',
        'Example Week 1: Getting Started',
        'Example Week 2: Get Interactive',
        'Example Week 3: Be Social',
        'About Exams and Certificates',
        'holding section',
    ]
