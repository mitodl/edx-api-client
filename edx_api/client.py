"""edX api client"""
from .course_structure import CourseStructure


def get_requester(credentials):
    """
    Returns an object to make authenticated requests. See python `requests` for
    the API.
    """
    return credentials['id']


# pylint: disable=too-few-public-methods
class EdxApi(object):
    """
    A client for speaking with edX.
    """
    def __init__(self, credentials, base_url='https://edx.org/'):
        if 'id' not in credentials:
            raise AttributeError("You must specify an `id` in your credentials")
        if 'secret' not in credentials:
            raise AttributeError(
                "You must specify a `secret` in your credentials")

        self.base_url = base_url
        self.credentials = credentials

    @property
    def course_structure(self):
        """Course Structure API"""
        return CourseStructure(get_requester(self.credentials), self.base_url)
