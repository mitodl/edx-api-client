"""Tests for CCX api"""
import json
import os.path
import requests

from mock import create_autospec
from .ccx import CCX


def test_create():
    """Test create method returns ccx id"""
    filename = os.path.join(os.path.dirname(__file__), 'fixtures/ccx_create_response.json')
    with open(filename) as f_obj:
        data = f_obj.read()

    mock_requester = create_autospec(requests)
    mock_requester.post.return_value.json.return_value = json.loads(data)
    ccx = CCX(mock_requester, 'https://example.org/')
    result = ccx.create('course-id', 'foo@bar.com', 100, 'test title')

    assert result == "ccx-v1:Organization+EX101+RUN-FALL2099+ccx@1"
