"""
Business objects for the course detail API
"""
from collections import namedtuple

from dateutil import parser
Media = namedtuple('Media', ['type', 'url'])


class CourseDetail(object):
    """
    The course detail object
    """
    def __init__(self, payload):
        self.json = payload

    def __str__(self):
        return "<Course detail for {}>".format(self.course_id)

    def __repr__(self):
        return self.__str__()

    @property
    def blocks_url(self):
        """Used to fetch the course blocks"""
        return self.json.get('blocks_url')

    @property
    def effort(self):
        """A textual description of the weekly hours of effort expected in the course."""
        return self.json.get('effort')

    @property
    def end(self):
        """Date the course ends"""
        try:
            return parser.parse(self.json.get('end'))
        except (AttributeError, TypeError):
            return None

    @property
    def enrollment_start(self):
        """Date enrollment begins"""
        try:
            return parser.parse(self.json.get('enrollment_start'))
        except (AttributeError, TypeError):
            return None

    @property
    def enrollment_end(self):
        """Date enrollment ends"""
        try:
            return parser.parse(self.json.get('enrollment_end'))
        except (AttributeError, TypeError):
            return None

    @property
    def course_id(self):
        """
        A unique identifier of the course; a serialized representation
        of the opaque key identifying the course.
        """
        return self.json.get('id')

    @property
    def name(self):
        """Name of the course"""
        return self.json.get('name')

    @property
    def number(self):
        """Catalog number of the course"""
        return self.json.get('number')

    @property
    def org(self):
        """Name of the organization that owns the course"""
        return self.json.get('org')

    @property
    def short_description(self):
        """A textual description of the course"""
        return self.json.get('short_description')

    @property
    def start(self):
        """Date the course begins"""
        try:
            return parser.parse(self.json.get('start'))
        except (AttributeError, TypeError):
            return None

    @property
    def start_display(self):
        """Readably formatted start of the course"""
        return self.json.get('start_display')

    @property
    def start_type(self):
        """
        Hint describing how `start_display` is set. One of:
            * `"string"`: manually set
            * `"timestamp"`: generated form `start` timestamp
            * `"empty"`: the start date should not be shown
        """
        return self.json.get('start_type')

    @property
    def overview(self):
        """
        A possibly verbose HTML textual description of the course.
        Note: this field is only included in the Course Detail view, not
        the Course List view.
        """
        return self.json.get('overview')

    @property
    def media(self):
        """Contains named media items"""
        for media_type, url_dict in self.json.get('media', {}).items():
            yield Media(type=media_type, url=url_dict.get('uri'))
