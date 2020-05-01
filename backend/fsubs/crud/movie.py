"""CRUD functions for movies."""

import logging
from typing import Any, Dict, List

from bson.objectid import ObjectId

from fsubs.models.video import VideoBaseInDB, VideoInstanceInDB

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
        LOGGER.debug(f'Creating movie: <{VideoBaseInDB}>.')
        return self.client.foreign_subs.movies.insert_one(movie).inserted_id

    def read(self, movie_id: str) -> Dict[str, Any]:
        """
        Read a movie.

        :param movie_id: The id of the movie to read.
        :returns: Dict representing the movie.
        """
        LOGGER.debug(f'Reading movie: <{movie_id}>.')
        movie = self.client.foreign_subs.movies.find_one({'_id': ObjectId(movie_id)})
        if movie:
            movie['id'] = str(movie.pop('_id'))
        return movie

    def read_multi(self, page_length) -> List[Dict[str, Any]]:
        """
        Read multiple movies.

        :param page_length: The number of movies to read.
        :returns: A list of Dicts representing movies.
        """
        LOGGER.debug(f'Reading all movies with page_length: <{page_length}>.')
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
        LOGGER.debug(f'Updating movie with uri: <{movie_id}> and movie: <{movie}>.')
        self.client.foreign_subs.movies.update({'_id': ObjectId(movie_id)}, {'$set': movie})

    def delete(self, movie_id: str):
        """
        Delete a movie.

        :param movie_id: The id of the movie to delete.
        """
        LOGGER.debug(f'Deleting movie: <{movie_id}>.')
        self.client.foreign_subs.movies.delete_one({'_id': ObjectId(movie_id)})

    def create_version(self, movie_version: VideoInstanceInDB) -> str:
        """
        Create a movie version.

        :param movie_version: A dict representing the movie version.
        :returns: The id of the newly created movie version.
        """
        LOGGER.debug(f'Creating movie version: <{movie_version}>.')
        return self.client.foreign_subs.movie_versions.insert_one(movie_version).inserted_id

    def read_version(self, movie_version_id: str) -> Dict[str, Any]:
        """
        Read a movie version.

        :param movie_version_id: The id of the movie to read.
        :returns: Dict representing the movie.
        """
        LOGGER.debug(f'Reading movie version: <{movie_version_id}>.')
        movie_version = self.client.foreign_subs.movie_versions.find_one(
            {'_id': ObjectId(movie_version_id)})
        if movie_version:
            movie_version['id'] = str(movie_version.pop('_id'))
        return movie_version

    def read_movie_version(self, movie_id: str) -> Dict[str, Any]:
        """
        Read all the versions of a movie.

        :param movie_version_id: The id of the movie to read.
        :returns: Dict representing the movie.
        """
        LOGGER.debug(f'Reading movie version: <{movie_id}>.')
        movie_versions = self.client.foreign_subs.movie_versions.find(
            {'video_base_id': str(movie_id)})
        versions = []
        for v in movie_versions:
            v['id'] = str(v.pop('_id'))
            versions.append(v)
        print(versions)
        return versions
