"""CRUD functions for movies."""

from models.video import VideoBase


class MovieDAO():
    """The DAO for interacting with movies."""

    def __init__(self, client):
        """Initialize a ``MovieDAO``."""
        self.client = client

    def create(self, movie: VideoBase):
        """Create a movie."""
        return self.client.foreign_subs.movies.insert_one(movie.dict()).inserted_id

    def read(self):
        """Read a movie."""
        raise NotImplementedError

    def update(self):
        """Update a movie."""
        raise NotImplementedError

    def delete(self):
        """Delete a movie."""
        raise NotImplementedError
