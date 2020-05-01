"""CRUD functions for movies."""

from backend.models.video import VideoBaseInDB

from bson.objectid import ObjectId


class MovieDAO():
    """The DAO for interacting with movies."""

    def __init__(self, client):
        """Initialize a ``MovieDAO``."""
        self.client = client

    def create(self, movie: VideoBaseInDB) -> str:
        """
        Create a movie.

        :param movie: A dict representing the movie.
        :returns: The id of the newly created movie.
        """
        return self.client.foreign_subs.movies.insert_one(movie).inserted_id

    def read(self, movie_id: str):
        """Read a movie."""
        movie = self.client.foreign_subs.movies.find_one({'_id': ObjectId(movie_id)})
        movie['_id'] = str(movie['_id'])
        return movie

    def read_multi(self, page_length):
        """Read a movie."""
        movies = self.client.foreign_subs.movies.find().limit(page_length)
        print(movies)
        #movies['_id'] = str(movie['_id'])
        return movies

    def update(self, movie_id: str, movie: VideoBaseInDB) -> str:
        """Update a movie."""
        return self.client.foreign_subs.movies.update({'_id': ObjectId(movie_id)}, {'$set': movie})

    def delete(self, movie_id: str):
        """Delete a movie."""
        self.client.foreign_subs.movies.delete_one({'_id': ObjectId(movie_id)})
