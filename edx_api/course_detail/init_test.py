"""Tests for Course Detail API"""

from unittest.mock import Mock
from urllib.parse import urljoin

import pytest

from edx_api.course_detail import CourseDetails, CourseModes
from edx_api.course_detail.models import CourseDetail, CourseMode


class TestCourseDetails:
    """Tests for CourseDetails class"""

    def setup_method(self):
        self.requester = Mock()
        self.base_url = "https://example.com"
        self.client = CourseDetails(self.requester, self.base_url)
        self.course_id = "course-v1:OpenedX+DemoX+DemoCourse"

    @pytest.mark.parametrize("username", [None, "testuser"])
    def test_get_detail_without_username(self, username):
        """Test getting course detail without username"""
        mock_response = Mock()
        mock_response.json.return_value = {"course_id": self.course_id}
        self.requester.get.return_value = mock_response

        result = self.client.get_detail(self.course_id, username=username)

        if username:
            self.requester.get.assert_called_once_with(
                urljoin(
                    self.base_url,
                    f"/api/courses/v1/courses/{self.course_id}/?username={username}",
                )
            )
        else:
            self.requester.get.assert_called_once_with(
                urljoin(self.base_url, f"/api/courses/v1/courses/{self.course_id}")
            )
        mock_response.raise_for_status.assert_called_once()
        assert isinstance(result, CourseDetail)


class TestCourseModes:
    """Tests for CourseModes class"""

    def setup_method(self):
        self.requester = Mock()
        self.base_url = "https://example.com"
        self.client = CourseModes(self.requester, self.base_url)
        self.course_id = "course-v1:OpenedX+DemoX+DemoCourse"

    def test_get_course_modes(self):
        """Test getting course modes"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"slug": "audit", "name": "Audit"},
            {"slug": "verified", "name": "Verified"},
        ]
        self.requester.get.return_value = mock_response

        result = self.client.get_course_modes(self.course_id)

        self.requester.get.assert_called_once_with(
            urljoin(self.base_url, f"/api/course_modes/v1/courses/{self.course_id}")
        )
        mock_response.raise_for_status.assert_called_once()
        assert len(result) == 2
        assert all(isinstance(mode, CourseMode) for mode in result)

    def test_get_mode_backwards_compatibility(self):
        """Test get_mode method for backwards compatibility"""
        mock_response = Mock()
        mock_response.json.return_value = [{"slug": "audit"}]
        self.requester.get.return_value = mock_response

        result = self.client.get_mode(self.course_id)

        assert len(result) == 1
        assert isinstance(result[0], CourseMode)

    def test_get_course_mode(self):
        """Test getting specific course mode"""
        mock_response = Mock()
        mock_response.json.return_value = {"slug": "verified", "name": "Verified"}
        self.requester.get.return_value = mock_response
        mode_slug = "verified"

        result = self.client.get_course_mode(self.course_id, mode_slug)

        self.requester.get.assert_called_once_with(
            urljoin(
                self.base_url,
                f"/api/course_modes/v1/courses/{self.course_id}/{mode_slug}",
            )
        )
        mock_response.raise_for_status.assert_called_once()
        assert isinstance(result, CourseMode)

    @pytest.mark.parametrize(
        "test_data",
        [
            {
                "mode_slug": "new_mode",
                "mode_display_name": "New Mode",
                "currency": "USD",
                "min_price": None,
                "expiration_datetime": None,
                "description": None,
                "sku": None,
                "bulk_sku": None,
                "expected_payload": {
                    "course_id": "course-v1:OpenedX+DemoX+DemoCourse",
                    "mode_slug": "new_mode",
                    "mode_display_name": "New Mode",
                    "currency": "USD",
                    "min_price": 0,
                },
            },
            {
                "mode_slug": "premium",
                "mode_display_name": "Premium Mode",
                "currency": "USD",
                "min_price": 100,
                "expiration_datetime": "2024-12-31T23:59:59Z",
                "description": "Premium access",
                "sku": "PREM001",
                "bulk_sku": "BULK001",
                "expected_payload": {
                    "course_id": "course-v1:OpenedX+DemoX+DemoCourse",
                    "mode_slug": "premium",
                    "mode_display_name": "Premium Mode",
                    "currency": "USD",
                    "min_price": 100,
                    "expiration_datetime": "2024-12-31T23:59:59Z",
                    "description": "Premium access",
                    "sku": "PREM001",
                    "bulk_sku": "BULK001",
                },
            },
        ],
    )
    def test_create_course_mode(self, test_data):
        """Test creating course mode with minimal and full parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {"slug": test_data["mode_slug"]}
        self.requester.post.return_value = mock_response

        # Filter out unwanted keys first
        filtered_items = {
            k: v
            for k, v in test_data.items()
            if k not in ["mode_slug", "mode_display_name", "currency", "expected_payload"]
        }
        # Then filter out None values
        kwargs = {k: v for k, v in filtered_items.items() if v is not None}

        result = self.client.create_course_mode(
            self.course_id,
            test_data["mode_slug"],
            test_data["mode_display_name"],
            test_data["currency"],
            **kwargs,
        )

        self.requester.post.assert_called_once_with(
            urljoin(self.base_url, f"/api/course_modes/v1/courses/{self.course_id}/"),
            json=test_data["expected_payload"],
        )
        mock_response.raise_for_status.assert_called_once()
        assert isinstance(result, CourseMode)

    @pytest.mark.parametrize(
        "status_code, should_succeed",
        [(204, True), (200, True), (400, False), (404, False)],
    )
    def test_update_course_mode(self, status_code, should_succeed):
        """Test updating course mode with different status codes"""
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = {"slug": "audit"}

        if not should_succeed:
            mock_response.raise_for_status.side_effect = Exception(
                f"HTTP {status_code} Error"
            )

        self.requester.patch.return_value = mock_response

        expected_payload = {
            "mode_display_name": "Updated Mode",
            "currency": "EUR",
            "min_price": 50,
        }

        if should_succeed:
            self.client.update_course_mode(
                self.course_id, "audit", "Updated Mode", "EUR", min_price=50
            )
        else:
            with pytest.raises(Exception):
                self.client.update_course_mode(
                    self.course_id, "audit", "Updated Mode", "EUR", min_price=50
                )

        self.requester.patch.assert_called_once_with(
            urljoin(
                self.base_url, f"/api/course_modes/v1/courses/{self.course_id}/audit"
            ),
            json=expected_payload,
            headers={"Content-Type": "application/merge-patch+json"},
        )

    @pytest.mark.parametrize(
        "mode_slug, status_code, is_success",
        [
            ("audit", 204, True),
            ("audit", 200, True),
            ("audit", 404, False),
            ("audit", 400, False),
        ],
    )
    def test_delete_course_mode(self, mode_slug, status_code, is_success):
        """Test deleting course mode with different status codes"""
        mock_response = Mock()
        mock_response.status_code = status_code

        if not is_success:
            mock_response.raise_for_status.side_effect = Exception(
                f"HTTP {status_code} Error"
            )

        self.requester.delete.return_value = mock_response

        if is_success:
            self.client.delete_course_mode(self.course_id, mode_slug)
        else:
            with pytest.raises(Exception):
                self.client.delete_course_mode(self.course_id, mode_slug)

        self.requester.delete.assert_called_once_with(
            urljoin(
                self.base_url,
                f"/api/course_modes/v1/courses/{self.course_id}/{mode_slug}",
            )
        )
        mock_response.raise_for_status.assert_called_once()
