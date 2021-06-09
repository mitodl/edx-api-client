"""Models for user_info client"""


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
