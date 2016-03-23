"""client tests"""
import pytest

from .client import EdxApi

def test_request_id_credential():
    """id key required in credentials"""
    with pytest.raises(AttributeError) as exc:
        EdxApi({})

    assert '`id`' in str(exc.value)

def test_request_secret_credential():
    """secret key required in credentials"""
    with pytest.raises(AttributeError) as exc:
        EdxApi({'id': 'asdf'})

    assert '`secret`' in str(exc.value)


def test_instantiation_happypath():
    """instantiatable with correct args"""
    EdxApi({'id': 'asdf', 'secret': 'jkl;'})
        