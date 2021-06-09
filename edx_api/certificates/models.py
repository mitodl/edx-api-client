"""
Business objects for the certificates API
"""
from dateutil import parser


class Certificates(object):
    """
    The certificates object
    This assumes that there can be only one certificate
    for a given course run and user.
    """
    def __init__(self, certificate_list):
        self.certificates = {}
        self.verified_certificates = {}
        for certificate in certificate_list:
            if not isinstance(certificate, Certificate):
                raise ValueError("Only Certificate objects are allowed")
            self.certificates[certificate.course_id] = certificate
            if certificate.is_verified:
                self.verified_certificates[certificate.course_id] = certificate

    def __str__(self):
        return "<Certificates>"

    @property
    def all_courses_certs(self):
        """Helper property to return all the course ids of the certificates"""
        return self.certificates.keys()

    @property
    def all_courses_verified_certs(self):
        """Helper property to return all the course ids of the verified certificates"""
        return self.verified_certificates.keys()

    @property
    def all_certs(self):
        """Helper property to return all the certificates"""
        return self.certificates.values()

    @property
    def all_verified_certs(self):
        """Helper property to return all the verified certificates"""
        return self.verified_certificates.values()

    def get_cert(self, course_id):
        """Returns the certificate for the given course id"""
        return self.certificates.get(course_id)

    def get_verified_cert(self, course_id):
        """Returns the verified certificate for the given course id"""
        return self.verified_certificates.get(course_id)

    def has_verified_cert(self, course_id):
        """Whether the course has a verified certificate"""
        return course_id in self.verified_certificates


class Certificate(object):
    """
    The certificate object
    """
    def __init__(self, json):
        self.json = json

    def __str__(self):
        return "<Certificate for user {username} for course {course_id}>".format(
            username=self.username,
            course_id=self.course_id
        )

    @property
    def is_verified(self):
        """Whether certificate_type is verified"""
        return self.certificate_type == 'verified'

    @property
    def username(self):
        """Returns the username property"""
        return self.json.get("username")

    @property
    def course_id(self):
        """Returns the course_id property"""
        return self.json.get("course_id")

    @property
    def certificate_type(self):
        """Returns the certificate_type property"""
        return self.json.get("certificate_type")

    @property
    def status(self):
        """Returns the status property"""
        return self.json.get("status")

    @property
    def download_url(self):
        """Returns the download_url property"""
        return self.json.get("download_url")

    @property
    def grade(self):
        """Returns the grade property"""
        return self.json.get("grade")

    @property
    def created(self):
        """Returns the created property"""
        return parser.parse(self.json.get('created'))

    @property
    def modified(self):
        """Returns the modified property"""
        return parser.parse(self.json.get('modified'))

    @property
    def is_passing(self):
        """Returns the is_passing property"""
        return self.json.get("is_passing")
