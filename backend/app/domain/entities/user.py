class User:
    """Represents a user within the domain."""
    def __init__(
        self,
        email: str,
        hashed_password: str,
        is_active: bool = True,
        is_superuser: bool = False,
    ):
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.is_superuser = is_superuser

    def activate(self):
        """Activates the user."""
        self.is_active = True

    def deactivate(self):
        """Deactivates the user."""
        self.is_active = False

    def set_superuser(self):
        """Grants superuser privileges."""
        self.is_superuser = True

    def remove_superuser(self):
        """Revokes superuser privileges."""
        self.is_superuser = False
