"""Models Tests for the Certificates API"""

from datetime import datetime
import os.path
import json
from unittest import TestCase

from .models import (
    Certificate,
    Certificates,
)


class CertificatesTests(TestCase):
    """Tests for certificates object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/certificates.json')) as file_obj:
            cls.certs_json = json.loads(file_obj.read())

        cls.certificates = Certificates([Certificate(cert_json) for cert_json in cls.certs_json])

    def test_str(self):
        """Test the __str__"""
        assert str(self.certificates) == "<Certificates>"

    def test_only_certificates(self):
        """Test that only certificates are allowed in the constructor"""
        with self.assertRaises(ValueError):
            Certificates(['foo', 'bar'])
        with self.assertRaises(ValueError):
            Certificates([{'foo': 'bar'}])

    def test_courses_cert(self):
        """Test for all_courses_certs"""
        assert sorted(list(self.certificates.all_courses_certs)) == sorted(
            ["course-v1:edX+DemoX+Demo_Course", "course-v1:MITx+8.MechCX+2014_T1"])

    def test_courses_verified_cert(self):
        """Test for all_courses_verified_certs"""
        assert list(self.certificates.all_courses_verified_certs) == [
            "course-v1:edX+DemoX+Demo_Course"
        ]

    def test_all_cert(self):
        """Test for all_certs"""
        all_certs = self.certificates.all_certs
        assert len(all_certs) == 2
        for cert in all_certs:
            assert isinstance(cert, Certificate)

    def test_all_verified_cert(self):
        """Test for all_verified_certs"""
        all_certs = list(self.certificates.all_verified_certs)
        assert len(all_certs) == 1
        assert isinstance(all_certs[0], Certificate)
        assert all_certs[0].course_id == "course-v1:edX+DemoX+Demo_Course"

    def test_get_certificate(self):
        """Test for get_cert"""
        assert self.certificates.get_cert('foo_id') is None
        assert isinstance(
            self.certificates.get_cert("course-v1:MITx+8.MechCX+2014_T1"),
            Certificate
        )

    def test_get_verified_cert(self):
        """Test for get_verified_cert"""
        assert self.certificates.get_verified_cert('foo_id') is None
        assert self.certificates.get_verified_cert("course-v1:MITx+8.MechCX+2014_T1") is None
        cert = self.certificates.get_verified_cert("course-v1:edX+DemoX+Demo_Course")
        assert isinstance(cert, Certificate)
        assert cert.is_verified is True

    def test_has_verified_cert(self):
        """Test for has_verified_cert"""
        assert self.certificates.has_verified_cert('foo_id') is False
        assert self.certificates.has_verified_cert(
            "course-v1:MITx+8.MechCX+2014_T1") is False
        assert self.certificates.has_verified_cert("course-v1:edX+DemoX+Demo_Course") is True


class CertificateTests(TestCase):
    """Tests for certificate object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/certificates.json')) as file_obj:
            cls.certs_json = json.loads(file_obj.read())

        cls.certificate = Certificate(cls.certs_json[0])

    def test_str(self):
        """Test the __str__"""
        assert str(self.certificate) == ("<Certificate for user bob for "
                                         "course course-v1:edX+DemoX+Demo_Course>")

    def test_is_verified(self):
        """Test for is_verified"""
        assert self.certificate.is_verified is True

    def test_username(self):
        """Test for username"""
        assert self.certificate.username == "bob"

    def test_course_id(self):
        """Test for course_id"""
        assert self.certificate.course_id == "course-v1:edX+DemoX+Demo_Course"

    def test_certificate_type(self):
        """Test for certificate_type"""
        assert self.certificate.certificate_type == "verified"

    def test_status(self):
        """Test for status"""
        assert self.certificate.status == "downloadable"

    def test_download_url(self):
        """Test for download_url"""
        assert self.certificate.download_url == "http://www.example.com/demo.pdf"

    def test_grade(self):
        """Test for grade"""
        assert self.certificate.grade == "0.98"

    def test_is_passing(self):
        """Test for is_passing"""
        assert self.certificate.is_passing is True

    def test_created(self):
        """Test for created"""
        expected = datetime.strptime(
            "2015-07-31T00:00:00", "%Y-%m-%dT%H:%M:%S"
        )
        assert self.certificate.created == expected

    def test_modified(self):
        """Test for modified"""
        expected = datetime.strptime(
            "2015-08-31T00:00:00", "%Y-%m-%dT%H:%M:%S"
        )
        assert self.certificate.modified == expected
