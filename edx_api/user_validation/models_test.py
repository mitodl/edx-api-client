"""Tests for UserValidationResult"""

import pytest

from .models import UserValidationResult


@pytest.mark.parametrize(
    "expected_value, validation_data, field",
    [
        ('Invalid name', {'validation_decisions': {'name': 'Invalid name'}}, 'name'),
        ('', {'validation_decisions': {'name': ''}}, 'name'),
        ('Invalid username', {'validation_decisions': {'username': 'Invalid username'}}, 'username'),
        ('', {'validation_decisions': {'username': ''}}, 'username'),
    ]
)
def test_properties(expected_value, validation_data, field):
    """Test properties on UserValidationResult model"""
    validation = UserValidationResult(validation_data)
    if field == 'name':
        assert validation.name == expected_value
    elif field == 'username':
        assert validation.username == expected_value


def test_str():
    """Test the __str__ method of UserValidationResult"""
    validation = UserValidationResult({'validation_decisions': {'name': ''}})
    assert str(validation) == "<User validation>"
