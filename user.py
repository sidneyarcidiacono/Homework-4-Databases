"""Import dependencies."""
from flask_login import UserMixin


# Define User class
class User(UserMixin):
    """Define User class based on UserMixIn."""

    def __init__(self, email, password, id):
        """Initialize user properties."""
        self.email = email
        self.password = password
        self.id = id
