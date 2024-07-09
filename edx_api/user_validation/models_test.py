"""Tests for Validation"""
import json
import os
from unittest import TestCase

from .models import Validation


class ValidationTests(TestCase):
    """Tests for Validation"""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/user_validation.json')) as file_obj:
            cls.user_validation_json = json.loads(file_obj.read())

        cls.validation_responses = cls.user_validation_json.get('validation_responses', {})

    def test_str(self):
        """Test the __str__"""
        self.assertEqual(str(self.get_validation_instance('valid_name')), "<User validation>")

    def test_properties(self):
        """Test properties on Validation model"""
        test_cases = [
            ('invalid_name', 'Invalid name', 'name'),
            ('valid_name', '', 'name'),
            ('invalid_username', 'Invalid username', 'username'),
            ('valid_username', '', 'username'),
        ]

        for key, expected_value, field in test_cases:
            with self.subTest(key=key):
                validation = self.get_validation_instance(key)
                if field == 'name':
                    self.assertEqual(validation.name, expected_value)
                elif field == 'username':
                    self.assertEqual(validation.username, expected_value)

    def get_validation_instance(self, key):
        return Validation(self.validation_responses.get(key, {}))
