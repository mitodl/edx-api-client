"""Course Detail API"""
from urllib.parse import urljoin

from .models import CourseDetail, CourseMode


# pylint: disable=too-few-public-methods
class CourseDetails:
    """
    API Client to interface with the course detail API.
    """

    def __init__(self, requester, base_url):
        self._requester = requester
        self._base_url = base_url

    def get_detail(self, course_id, username=None):
        """
        Fetches course details.

        Args:
            course_id (str): An edx course id.

        Returns:
            CourseDetail
        """
        # the request is done on behalf of the current logged in user
        # this only works if COURSE_ABOUT_VISIBILITIY_PERMISSION is not
        # set to staff, otherwise you need to pass in a username with
        # permissions.
        if not username:
            resp = self._requester.get(
                urljoin(
                    self._base_url,
                    f"/api/courses/v1/courses/{course_id}",
                )
            )
        else:
            resp = self._requester.get(
                urljoin(
                    self._base_url,
                    f"/api/courses/v1/courses/{course_id}/?username={username}"
                )
            )

        resp.raise_for_status()

        return CourseDetail(resp.json())


class CourseModes:
    """
    API Client to interface with the course modes API.
    """

    def __init__(self, requester, base_url):
        self._requester = requester
        self._base_url = base_url

    def get_course_modes(self, course_id):
        """
        Fetches details of all the course modes for a single course.

        Args:
            course_id (str): An edx course id.

        Returns:
            List of CourseMode
        """
        resp = self._requester.get(
            urljoin(
                self._base_url,
                f"/api/course_modes/v1/courses/{course_id}",
            )
        )

        resp.raise_for_status()
        course_mode_list = []
        for course_mode_json in resp.json():
            course_mode_list.append(CourseMode(course_mode_json))
        return course_mode_list

    def get_mode(self, course_id):
        """
        Just for backwards compatibility, fetches course mode details.
        """
        return self.get_course_modes(course_id)

    def get_course_mode(self, course_id, mode_slug):
        """
        Fetches a specific course mode details.

        Args:
            course_id (str): An edx course id.
            mode_slug (str): The mode slug to fetch.

        Returns:
            CourseMode
        """
        resp = self._requester.get(
            urljoin(
                self._base_url,
                f"/api/course_modes/v1/courses/{course_id}/{mode_slug}",
            )
        )

        resp.raise_for_status()
        return CourseMode(resp.json())

    def create_course_mode(self, course_id, mode_slug, mode_display_name, currency, min_price=0, expiration_datetime=None, description=None, sku=None, bulk_sku=None):
        """
        Creates a new course mode for the given course.

        Args:
            course_id (str): An edx course id.
            mode_slug (str): The mode slug to create.
            mode_display_name (str): The mode display name to create.
            currency (str): The currency for the price.
            min_price (Decimal): The minimum price for the mode.
            expiration_datetime (str, optional): The expiration datetime for the mode in ISO 8601 format. Defaults to None.
            description (str, optional): A description for the mode. Defaults to None.
            sku (str, optional): The SKU for the mode. Defaults to None.
            bulk_sku (str, optional): The bulk SKU for the mode. Defaults to None

        Returns:
            CourseMode: The created course mode.
        """
        payload = {
            "course_id": course_id,
            "mode_slug": mode_slug,
            "mode_display_name": mode_display_name,
            "currency": currency,
            "min_price": min_price,
        }

        optional_fields = {
            "expiration_datetime": expiration_datetime,
            "description": description,
            "sku": sku,
            "bulk_sku": bulk_sku,
        }
        payload.update({k: v for k, v in optional_fields.items() if v is not None})
        
        resp = self._requester.post(
            urljoin(
                self._base_url,
                f"/api/course_modes/v1/courses/{course_id}/",
            ),
            json=payload
        )
        resp.raise_for_status()
        return CourseMode(resp.json())

    def update_course_mode(self, course_id, mode_slug, mode_display_name=None, currency=None, min_price=None, expiration_datetime=None, description=None, sku=None, bulk_sku=None):
        """
        Updates an existing course mode for the given course.

        Args:
            course_id (str): An edx course id.
            mode_slug (str): The mode slug to update.
            mode_display_name (str): The mode display name to update.
            min_price (Decimal): The new minimum price for the mode.
            currency (str): The new currency for the price.
            expiration_datetime (str, optional): The new expiration datetime for the mode in ISO 8601 format. Defaults to None.
            description (str, optional): The new description for the mode. Defaults to None.
            sku (str, optional): The new SKU for the mode. Defaults to None.
            bulk_sku (str, optional): The new bulk SKU for the mode. Defaults to None.
        Returns:
             None: On successful update.
        """
        payload = {
            "mode_display_name": mode_display_name,
            "currency": currency,
            "min_price": min_price,
            "expiration_datetime": expiration_datetime,
            "description": description,
            "sku": sku,
            "bulk_sku": bulk_sku,
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        resp = self._requester.patch(
            urljoin(
            self._base_url,
            f"/api/course_modes/v1/courses/{course_id}/{mode_slug}",
            ),
            json=payload,
            headers={"Content-Type": "application/merge-patch+json"}
        )
        resp.raise_for_status()
        return

    def delete_course_mode(self, course_id, mode_slug):
        """
        Deletes an existing course mode for the given course.

        Args:
            course_id (str): An edx course id.
            mode_slug (str): The mode slug to delete.
        Returns:
            None: On successful deletion.
        """
        resp = self._requester.delete(
            urljoin(
                self._base_url,
                f"/api/course_modes/v1/courses/{course_id}/{mode_slug}",
            )
        )
        resp.raise_for_status()
        return
