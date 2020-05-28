"""CRUD functions for tv shows."""

import logging
from typing import Any, Dict

from bson.objectid import ObjectId

from fsubs.models.video import VideoBaseInDB

LOGGER = logging.getLogger(__name__)


class TVShowDAO():
    """The DAO for interacting with users."""

    def __init__(self, client):
        """
        Initialize a ``TVShowDAO``.

        :param client: The MongoClient object ot use for the DAO.
        """
        self.client = client

    def create(self, tv_show: VideoBaseInDB) -> str:
        """
        Create a TV Show.

        :param user: The ``VideoBaseInDB`` object representing the tv show to create.
        :returns: The id of the newly created tv show.
        """
        LOGGER.debug('Creating tv show from DAO.')
        return self.client.foreign_subs.tv_shows.insert_one(tv_show).inserted_id

    def read(self, tv_show_id: str) -> Dict[str, Any]:
        """
        Read a tv show.

        :param tv_show_id: The id of the tv show to read.
        :returns: Dict representing the tv show.
        """
        LOGGER.debug(f'Reading tv show: <{tv_show_id}>.')
        tv_show = self.client.foreign_subs.tv_shows.find_one({'_id': ObjectId(tv_show_id)})
        if tv_show:
            tv_show['id'] = str(tv_show.pop('_id'))
        return tv_show
