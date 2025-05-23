"""
Business objects for the course run API
"""

from dateutil import parser


class CourseRun:
    """
    The course run object
    """

    def __init__(self, payload):
        self.json = payload

    def __str__(self):
        return f"<Course run details for {self.course_id}>"

    def __repr__(self):
        return self.__str__()

    @property
    def schedule(self):
        """Used to fetch the course schedule"""
        return self.json.get("schedule")

    @property
    def start(self):
        """Date the course run begins"""
        try:
            return parser.parse(self.schedule.get("start"))
        except (AttributeError, TypeError):
            return None

    @property
    def end(self):
        """Date the course run ends"""
        try:
            return parser.parse(self.schedule.get("end"))
        except (AttributeError, TypeError):
            return None

    @property
    def enrollment_start(self):
        """Date enrollment begins"""
        try:
            return parser.parse(self.schedule.get("enrollment_start"))
        except (AttributeError, TypeError):
            return None

    @property
    def enrollment_end(self):
        """Date enrollment ends"""
        try:
            return parser.parse(self.schedule.get("enrollment_end"))
        except (AttributeError, TypeError):
            return None

    @property
    def pacing_type(self):
        """
        Pacing type of a course. Possible values are ("instructor_paced" or "self_paced")
        """
        return self.json.get("pacing_type")

    @property
    def course_id(self):
        """
        A unique identifier of the course; a serialized representation
        of the opaque key identifying the course.
        """
        return self.json.get("id")

    @property
    def title(self):
        """Title of the course"""
        return self.json.get("title")

    @property
    def card_image(self):
        """Card image of the course"""
        return self.json.get("images").get("card_image")

    @property
    def org(self):
        """Name of the organization that owns the course"""
        return self.json.get("org")

    @property
    def number(self):
        """Course number of the course"""
        return self.json.get("number")

    @property
    def run(self):
        """Run number of the course"""
        return self.json.get("run")


class CourseRunList:
    """
    A list of course runs
    """

    def __init__(self, payload):
        self.json = payload

    @property
    def next(self):
        """
        Returns the next page of course runs list
        """
        return self.json.get("next", None)

    @property
    def previous(self):
        """
        Returns the previous page of course runs list
        """
        return self.json.get("previous", None)

    @property
    def count(self):
        """
        Returns the number of course runs
        """
        return self.json.get("count", 0)

    @property
    def num_pages(self):
        """
        Returns the number of pages of course runs list
        """
        return self.json.get("num_pages", 0)

    @property
    def current_page(self):
        """
        Returns the current page of course runs list
        """
        return self.json.get("current_page", 0)

    @property
    def start(self):
        """
        Returns the start of the pagination
        """
        return self.json.get("start", None)

    @property
    def results(self):
        """
        Returns a list of course runs
        """
        return [CourseRun(course_run) for course_run in self.json.get("results", [])]
