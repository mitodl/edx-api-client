"""
API Client for interacting w/ CCXs
"""
import logging
from urllib import parse


log = logging.getLogger(__name__)


class CCX(object):
    """
    API Client for interacting w/ CCXs
    """
    def __init__(self, requester, base_url):
        self.requester = requester
        self.base_url = base_url

    # pylint: disable=too-many-arguments
    def create(self, master_course_id, coach_email, max_students_allowed, title, modules=None):
        """
        Creates a CCX

        Args:
            master_course_id (str): edx course id of the master course
            coach_email (str): email of the user to make a coach. This user must exist on edx.
            max_students_allowed (int): Maximum number of students to allow in this ccx.
            title (str): Title of the CCX to be created
            modules (optional list): A list of locator_ids (str) for the modules to enable.

        Returns:
           ccx_id (str): The ID of the ccx.
        """
        payload = {
            'master_course_id': master_course_id,
            'coach_email': coach_email,
            'max_students_allowed': max_students_allowed,
            'display_name': title,
        }

        if modules is not None:
            payload['course_modules'] = modules

        resp = self.requester.post(
            parse.urljoin(self.base_url, '/api/ccx/v0/ccx/'),
            json=payload
        )

        try:
            resp.raise_for_status()
        except Exception:
            log.error(resp.json())
            raise

        return resp.json()['ccx_course_id']
