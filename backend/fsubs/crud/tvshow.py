"""CRUD functions for TV shows."""

import logging
from typing import Any, Dict, List

from bson.objectid import ObjectId

from fsubs.models.video import VideoBaseInDB
from fsubs.models.tvshow import TVShowEpisodeInDB

LOGGER = logging.getLogger(__name__)


class TVShowDAO():
    """The DAO for interacting with users."""

    def __init__(self, client):
        """
        Initialize a ``TVShowDAO``.

        :param client: The MongoClient object ot use for the DAO.
        """
        self.client = client

    async def create(self, tv_show: VideoBaseInDB) -> str:
        """
        Create a tv Show.

        :param user: The ``VideoBaseInDB`` object representing the tv show to create.
        :returns: The id of the newly created tv show.
        """
        LOGGER.debug('Creating tv show from DAO.')
        return self.client.foreign_subs.tv_shows.insert_one(tv_show).inserted_id

    async def read(self, tv_show_id: str) -> Dict[str, Any]:
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

    async def read_multi(self, limit=100, skip=0) -> List[Dict[str, Any]]:
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

    async def update(self, tv_show_id: str, tv_show: VideoBaseInDB):
        """
        Update a tv show.

        :param tv_show_id: The id of the tv show to update.
        :param tv_show: The tv show data to update with.
        """
        LOGGER.debug(f'Updating tv show with uri: <{tv_show_id}> and tv_show: <{tv_show}>.')
        self.client.foreign_subs.tv_show.update({'_id': ObjectId(tv_show_id)}, {'$set': tv_show})

    async def delete(self, tv_show_id: str):
        """
        Delete a tv show.

        :param tv_show_id: The id of the tv show to delete.
        """
        LOGGER.debug(f'Deleting tv show: <{tv_show_id}>.')
        self.client.foreign_subs.tv_shows.delete_one({'_id': ObjectId(tv_show_id)})

    async def create_episode(self, episode: TVShowEpisodeInDB) -> str:
        """
        Create a tv episode.

        :param episode: The ``TVShowEpisodeInDB`` object representing the tv episode to create.
        :returns: The id of the newly created tv episode.
        """
        LOGGER.debug('Creating tv episode from DAO.')
        return self.client.foreign_subs.tv_show_episodes.insert_one(episode).inserted_id

    async def read_episode(self, episode_id: str) -> Dict[str, Any]:
        """
        Read a tv episode.

        :param episode_id: The id of the tv episode to read.
        :returns: Dict representing the tv episode.
        """
        LOGGER.debug(f'Reading tv episode: <{episode_id}>.')
        tv_episode = self.client.foreign_subs.tv_show_episodes.find_one(
            {'_id': ObjectId(episode_id)})
        if tv_episode:
            tv_episode['id'] = str(tv_episode.pop('_id'))
        return tv_episode

    async def read_tv_show_episodes(self, tv_show_id: str) -> List[Dict[str, Any]]:
        """
        Read all tv episodes for a tv show.

        :param tv_show_id: The id of the tv show to read episodes for.
        :returns: Dict representing all the tv episodes for the tv show.
        """
        LOGGER.debug(f'Reading tv episodes for tv_show_id: {tv_show_id}.')
        tv_episodes = self.client.foreign_subs.tv_show_episodes.find(
            {'video_base_id': tv_show_id})
        tv_episodes = list(tv_episodes)
        for episode in tv_episodes:
            episode['id'] = str(episode.pop('_id'))
        print(f'Found episodes: {tv_episodes}.')
        return tv_episodes

    async def update_episode(self, episode_id: str, episode: TVShowEpisodeInDB):
        """
        Update a tv episode.

        :param episode_id: The id of the tv episode to update.
        :param episode: The episode data to update with.
        """
        LOGGER.debug(f'Updating tv episode with uri: <{episode_id}> and episode: <{episode}>.')
        self.client.foreign_subs.tv_show_episodes.update(
            {'_id': ObjectId(episode_id)}, {'$set': episode})

    async def delete_episode(self, episode_id: str):
        """
        Delete a tv episode.

        :param episode_id: The id of the episode to delete.
        """
        LOGGER.debug(f'Deleting tv episode: <{episode_id}>.')
        self.client.foreign_subs.tv_show_episodes.delete_one({'_id': ObjectId(episode_id)})
