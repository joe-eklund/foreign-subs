"""CRUD functions for tv shows."""

import logging

from fsubs.models.tvshow import TVShowInDB

LOGGER = logging.getLogger(__name__)


class TVShowDAO():
    """The DAO for interacting with users."""

    def __init__(self, client):
        """
        Initialize a ``TVShowDAO``.

        :param client: The MongoClient object ot use for the DAO.
        """
        self.client = client

    def create(self, tv_show: TVShowInDB) -> str:
        """
        Create a TV Shows.

        :param user: The ``TVShowInDB`` object representing the tv show to create.
        :returns: The id of the newly created tv show.
        """
        LOGGER.debug('Creating tv show from DAO.')
        return self.client.foreign_subs.tv_shows.insert_one(tv_show).inserted_id
