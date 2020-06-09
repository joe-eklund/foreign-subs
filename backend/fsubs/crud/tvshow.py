"""CRUD functions for tv shows."""

import logging
from typing import Any, Dict, List

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

    def read_multi(self, limit=100, skip=0) -> List[Dict[str, Any]]:
        """
        Read multiple tv shows.

        :param limit: The number of tv shows to read.
        :param skip: The number of tv shows to skip.
        :returns: A list of Dicts representing tv shows.
        """
        LOGGER.debug(f'Reading all tv shows with limit: <{limit}> and skip: <{skip}>.')
        tv_shows = self.client.foreign_subs.tv_shows.find().skip(skip).limit(limit)
        tv_shows = list(tv_shows)
        for tv_show in tv_shows:
            tv_show['id'] = str(tv_show.pop('_id'))
        return tv_shows

    def update(self, tv_show_id: str, tv_show: VideoBaseInDB):
        """
        Update a tv show.

        :param tv_show_id: The id of the tv show to update.
        :param tv_show: The tv show data to update with.
        """
        LOGGER.debug(f'Updating tv show with uri: <{tv_show_id}> and tv_show: <{tv_show}>.')
        self.client.foreign_subs.tv_show.update({'_id': ObjectId(tv_show_id)}, {'$set': tv_show})

    def delete(self, tv_show_id: str):
        """
        Delete a tv show.

        :param tv_show_id: The id of the tv show to delete.
        """
        LOGGER.debug(f'Deleting tv show: <{tv_show_id}>.')
        self.client.foreign_subs.tv_shows.delete_one({'_id': ObjectId(tv_show_id)})

    def create_episode(self, episode: VideoBaseInDB) -> str:
        """
        Create a TV Episode.

        :param user: The ``VideoBaseInDB`` object representing the tv episode to create.
        :returns: The id of the newly created tv episode.
        """
        LOGGER.debug('Creating tv episode from DAO.')
        return self.client.foreign_subs.tv_show_episodes.insert_one(episode).inserted_id
