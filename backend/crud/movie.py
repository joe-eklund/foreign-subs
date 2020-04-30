"""CRUD functions for movies."""


class MovieDAO():
    """The DAO for interacting with movies."""

    def __init__(self, client):
        """Initialize a ``MovieDAO``."""
        self.client = client

    def create(self):
        """Create a movie."""
        raise NotImplementedError

    def read(self):
        """Read a movie."""
        raise NotImplementedError

    def update(self):
        """Update a movie."""
        raise NotImplementedError

    def delete(self):
        """Delete a movie."""
        raise NotImplementedError
