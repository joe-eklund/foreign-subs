"""CRUD functions for movies."""

from models.video import VideoBaseResponse

from bson.objectid import ObjectId


class MovieDAO():
    """The DAO for interacting with movies."""

    def __init__(self, client):
        """Initialize a ``MovieDAO``."""
        self.client = client

    def create(self, movie: VideoBaseResponse) -> str:
        """
        Create a movie.

        :param movie: A dict representing the movie.
        :returns: The id of the newly created movie.
        """
        return self.client.foreign_subs.movies.insert_one(movie).inserted_id

    def read(self, movie_id: str):
        """Read a movie."""
        return self.client.foreign_subs.movies.find_one({'_id': ObjectId(movie_id)})

    def update(self):
        """Update a movie."""
        raise NotImplementedError

    def delete(self):
        """Delete a movie."""
        raise NotImplementedError
