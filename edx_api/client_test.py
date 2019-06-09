"""client tests"""
import pytest

from .client import EdxApi


def test_request_id_credential():
    """access_token required in credentials"""
    with pytest.raises(AttributeError) as exc:
        EdxApi({})

    assert 'access token' in str(exc.value)


def test_instantiation_happypath():
    """instantiatable with correct args"""
    token = 'asdf'
    api_key = 'api_key'
    client = EdxApi({'access_token': token, 'api_key': api_key})
    assert client.get_requester().headers['Authorization'] == 'Bearer {token}'.format(token=token)
    assert client.get_requester().headers['X-EdX-Api-Key'] == api_key
