"""Tests for Info"""
import json
import os
from unittest import TestCase

from .models import Info


class InfoTests(TestCase):
    """Tests for Info"""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/user_info.json')) as file_obj:
            cls.user_info_json = json.loads(file_obj.read())

        cls.info = Info(cls.user_info_json)

    def test_str(self):
        """Test the __str__"""
        assert str(self.info) == "<User info for user staff>"

    def test_properties(self):
        """Test properties on Info model"""
        assert self.info.name == self.user_info_json['name']
        assert self.info.username == self.user_info_json['username']
        assert self.info.email == self.user_info_json['email']
        assert self.info.user_id == self.user_info_json['id']

    def test_missing(self):  # pylint: disable=no-self-use
        """Missing properties shouldn't cause a problem"""
        info = Info({})

        assert info.name is None
        assert info.username is None
        assert info.email is None
        assert info.user_id is None
