"""Models for user_info client"""
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class Info(object):
    """
    Information about user
    """
    def __init__(self, json):
        self.json = json

    def __str__(self):
        return "<User info for user {user}>".format(
            user=self.username,
        )

    @property
    def username(self):
        """Returns the username of the user."""
        return self.json.get('username')

    @property
    def email(self):
        """Email for the user"""
        return self.json.get('email')

    @property
    def name(self):
        """Name for the user"""
        return self.json.get('name')

    @property
    def user_id(self):
        """Id for the user"""
        return self.json.get('id')

    @property
    def bio(self):
        """
        null or textual representation of user biographical information
        """
        return self.json.get('bio')

    @property
    def country(self):
        """An ISO 3166 country code or null."""
        return self.json.get('country')

    @property
    def requires_parental_consent(self):
        """If the user is a minor"""
        return self.json.get('requires_parental_consent')

    @property
    def level_of_education(self):
        """
        Returns one of the following values:
            "p": PhD or Doctorate
            "m": Master's or professional degree
            "b": Bachelor's degree
            "a": Associate's degree
            "hs": Secondary/high school
            "jhs": Junior secondary/junior high/middle school
            "el": Elementary/primary school
            "none": None
            "o": Other
            null: The user did not enter a value
        """
        return self.json.get('level_of_education')

    @property
    def goals(self):
        return self.json.get('goals')

    @property
    def language_proficiencies(self):
        """
        Returns array of language preferences
        """
        return self.json.get('language_proficiencies')

    @property
    def gender(self):
        return self.json.get('gender')

    @property
    def is_active(self):
        """Boolean representation of whether a user is active."""
        return self.json.get('is_active')
