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

        :param movie: The ``VideoBaseInDB`` object representing the movie to create.
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

    def read_multi(self, limit=100, skip=0) -> List[Dict[str, Any]]:
        """
        Read multiple movies.

        :param limit: The number of movies to read.
        :param skip: The number of movies to skip.
        :returns: A list of Dicts representing movies.
        """
        LOGGER.debug(f'Reading all movies with limit: <{limit}> and skip: <{skip}>.')
        movies = self.client.foreign_subs.movies.find().skip(skip).limit(limit)
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

    def read_movie_versions(self, movie_id: str) -> Dict[str, Any]:
        """
        Read all the versions of a movie.

        :param movie_version_id: The id of the movie to read.
        :returns: Dict representing the movie.
        """
        LOGGER.debug(f'Reading movie versions for: <{movie_id}>.')
        movie_versions = self.client.foreign_subs.movie_versions.find(
            {'video_base_id': str(movie_id)})
        versions = []
        for v in movie_versions:
            v['id'] = str(v.pop('_id'))
            versions.append(v)
        return versions

    def update_version(self, movie_version_id: str, movie_version) -> VideoInstanceInDB:
        """
        Update a movie version.

        :param movie_id: The id of the movie version to update.
        :param movie_version: The movie version data to update with.
        """
        LOGGER.debug(f'Updating movie version with uri: <{movie_version_id}> and movie_version: '
                     f'<{movie_version}>.')
        self.client.foreign_subs.movie_versions.update(
            {'_id': ObjectId(movie_version_id)},
            {'$set': movie_version})

    def delete_version(self, movie_version_id: str):
        """
        Delete a movie version.

        :param movie_id: The id of the movie to delete.
        """
        LOGGER.debug(f'Deleting movie version: <{movie_version_id}>.')
        self.client.foreign_subs.movie_versions.delete_one({'_id': ObjectId(movie_version_id)})

    def delete_movie_versions(self, movie_id: str):
        """
        Delete all the versions of a movie.

        :param movie_version_id: The id of the movie to delete with.
        """
        LOGGER.debug(f'Deleting movie version for: <{movie_id}>.')
        self.client.foreign_subs.movie_versions.delete_many({'video_base_id': str(movie_id)})
