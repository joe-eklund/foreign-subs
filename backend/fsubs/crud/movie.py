"""CRUD functions for movies."""

import logging

from typing import Any, Dict, List

from fsubs.models.video import VideoBaseInDB

from bson.objectid import ObjectId

LOGGER = logging.getLogger(__name__)


class MovieDAO():
    """The DAO for interacting with movies."""

    def __init__(self, client):
        """
        Initialize a ``MovieDAO``.

        :param client: The MongoClient object to use for the DAO.
        """
        self.client = client

    def create(self, movie: VideoBaseInDB) -> str:
        """
        Create a movie.

        :param movie: A dict representing the movie.
        :returns: The id of the newly created movie.
        """
        return self.client.foreign_subs.movies.insert_one(movie).inserted_id

    def read(self, movie_id: str) -> Dict[str, Any]:
        """
        Read a movie.

        :param movie_id: The id of the movie to read.
        :returns: Dict representing the movie.
        """
        movie = self.client.foreign_subs.movies.find_one({'_id': ObjectId(movie_id)})
        if movie:
            movie['id'] = str(movie['_id'])
        return movie

    def read_multi(self, page_length) -> List[Dict[str, Any]]:
        """
        Read multiple movies.

        :param page_length: The number of movies to read.
        :returns: A list of Dicts representing movies.
        """
        movies = self.client.foreign_subs.movies.find().limit(page_length)
        movies = list(movies)
        for movie in movies:
            movie['id'] = str(movie.pop('_id'))
        return movies

    def update(self, movie_id: str, movie: VideoBaseInDB):
        """
        Update a movie.

        :param movie_id: The id of the movie to update.
        :param movie: The movie data to update with.
        """
        self.client.foreign_subs.movies.update({'_id': ObjectId(movie_id)}, {'$set': movie})

    def delete(self, movie_id: str):
        """
        Delete a movie.

        :param movie_id: The id of the movie to delete.
        """
        self.client.foreign_subs.movies.delete_one({'_id': ObjectId(movie_id)})
