"""Models for user_info client"""


class Info:
    """
    Information about user
    """
    def __init__(self, json):
        self.json = json

    def __str__(self):
        return f"<User info for user {self.username}>"

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
