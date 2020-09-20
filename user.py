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

    def is_anonymous(self):
        """Set is_anonymous for logged-in user."""
        return False

    def is_authenticated(self):
        """Set is_authenticated for logged-in user."""
        return True
