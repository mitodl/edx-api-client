"""Models for user_validation client"""


class UserValidationResult(object):
    """
    Validation result about user
    """
    def __init__(self, json):
        self.validation_decisions = json.get('validation_decisions', {})

    def __str__(self):
        return f"<User validation>"

    @property
    def name(self):
        """
        Returns name validation of the user

        Returns:
            str: A validation message for the name. An empty string indicates a valid name.
        """
        return self.validation_decisions.get('name')

    @property
    def username(self):
        """
        Returns username validation of the user.

        Returns:
            str: A validation message for the username. An empty string indicates a valid username.
        """
        return self.validation_decisions.get('username')
