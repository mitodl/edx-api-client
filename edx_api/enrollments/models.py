"""
Business objects for the enrollments API
"""
from dateutil import parser

# pylint: disable=too-few-public-methods


class Enrollments(object):
    """
    The enrollments object
    """

    def __init__(self, payload):
        self.enrollments = {}
        for enrollment_json in payload:
            enrollment = Enrollment(enrollment_json)
            self.enrollments[enrollment.course_id] = enrollment

    def __str__(self):
        return "<Enrollments>"

    @property
    def enrolled_courses(self):
        """
        Returns a iterable of all the courses the user has enrolled in
        """
        return self.enrollments.values()

    def get_enrolled_courses_by_ids(self, course_id_list):
        """
        Helper function to pull the enrolled courses information for only the
        course ids specified in course_id_list

        Args:
            course_id_list (List): list of course IDs

        Returns:
            generator of Enrollment objects
        """
        if not isinstance(course_id_list, (list, tuple)):
            raise ValueError('course_id_list should be an instance of list or tuple')
        for course_id in course_id_list:
            yield self.enrollments.get(course_id)

    def get_enrolled_course_ids(self, filter_by_id_list=None):
        """
        Helper function that extracts the course id only from the course IDs
        Args:
            filter_by_id_list (List): list of course IDs

        Returns:
            iterable of strings representing course IDs
        """
        all_ids = self.enrollments.keys()
        if filter_by_id_list is not None:
            all_ids = set(all_ids).intersection(set(filter_by_id_list))
        return all_ids

    def is_enrolled_in(self, course_id):
        """
        Helper to check if the provided course id is in the enrollments

        Args:
            course_id (str): a string representing a course id

        Returns:
            bool: whether an enrollment for the provided course id exists
        """
        return course_id in self.enrollments

    def get_enrollment_for_course(self, course_id):
        """
        Helper to get a specific enrollment for a course_id
        """
        return self.enrollments.get(course_id)


class Enrollment(object):
    """
    Single enrollment object representation
    """
    def __init__(self, json):
        self.json = json

    def __str__(self):
        return "<Enrollment for user {user} in course {course}>".format(
            user=self.user,
            course=self.course_id
        )

    @property
    def course_id(self):
        """Shortcut for a nested property"""
        return self.course_details.course_id or self.json.get('course_id')

    @property
    def created(self):
        """Returns a datetime object of the enrollment timestamp"""
        try:
            return parser.parse(self.json.get('created'))
        except (AttributeError, TypeError):
            return None

    @property
    def mode(self):
        """Returns the enrollment mode of the user in this course"""
        return self.json.get('mode')

    @property
    def is_active(self):
        """Returns whether the enrollment is currently active."""
        return self.json.get('is_active') is True

    @property
    def course_details(self):
        """Returns a CourseDetails object"""
        return CourseDetails(self.json.get('course_details', {}))

    @property
    def user(self):
        """Returns the username of the user."""
        return self.json.get('user')

    @property
    def is_verified(self):
        """
        Checks if the mode is "verified"
        """
        return self.mode == 'verified'


class CourseDetails(object):
    """
    Course enrollment info
    """
    def __init__(self, json):
        self.json = json

    def __str__(self):
        return "<Enrollment details for course {}>".format(self.course_id)

    @property
    def course_id(self):
        """Returns the unique identifier for the course."""
        return self.json.get('course_id')

    @property
    def course_start(self):
        """
        Returns the date and time when the course opens.
        If None, the course opens immediately when it is created.
        """
        try:
            return parser.parse(self.json.get('course_start'))
        except (AttributeError, TypeError):
            return None

    @property
    def course_end(self):
        """
        Returns the date and time when the course closes.
        If None, the course never ends.
        """
        try:
            return parser.parse(self.json.get('course_end'))
        except (AttributeError, TypeError):
            return None

    @property
    def enrollment_start(self):
        """
        Returns the date and time when users can begin enrolling in the course.
        If None, enrollment opens immediately when the course is created.
        """
        try:
            return parser.parse(self.json.get('enrollment_start'))
        except (AttributeError, TypeError):
            return None

    @property
    def enrollment_end(self):
        """
        Returns the date and time after which users cannot enroll for the course.
        If None, the enrollment period never ends.
        """
        try:
            return parser.parse(self.json.get('enrollment_end'))
        except (AttributeError, TypeError):
            return None

    @property
    def invite_only(self):
        """
        Returns a boolean indicating whether students
        must be invited to enroll in the course.
        """
        return self.json.get('invite_only') is True

    @property
    def course_modes(self):
        """
        Returns a generator of data about the enrollment
        modes supported for the course.
        """
        for course_mode_json in self.json.get('course_modes', []):
            yield CourseMode(course_mode_json)


class CourseMode(object):
    """
    Course enrollment mode
    """
    def __init__(self, json):
        self.json = json

    def __str__(self):
        return "<Enrollment mode {}>".format(self.slug)

    @property
    def currency(self):
        """Returns the currency of the listed prices."""
        return self.json.get('currency')

    @property
    def description(self):
        """Returns a description of this mode."""
        return self.json.get('description')

    @property
    def expiration_datetime(self):
        """
        Returns the date and time after which users
        cannot enroll in the course in this mode.
        """
        try:
            return parser.parse(self.json.get('expiration_datetime'))
        except (AttributeError, TypeError):
            return None

    @property
    def min_price(self):
        """Returns the minimum price for which a user can enroll in this mode."""
        return self.json.get('min_price')

    @property
    def name(self):
        """Returns the full name of the enrollment mode."""
        return self.json.get('name')

    @property
    def slug(self):
        """Returns the short name for the enrollment mode."""
        return self.json.get('slug')

    @property
    def suggested_prices(self):
        """Returns a list of suggested prices for this enrollment mode."""
        return self.json.get('suggested_prices')
