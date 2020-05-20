"""REST API tv show functions."""

import logging
from typing import List

from fastapi import APIRouter, Query
from pymongo import MongoClient

from fsubs.config.config import config
from fsubs.crud.tvshow import TVShowDAO
from fsubs.models.misc import ObjectIdStr
from fsubs.models.tvshow import TVShow, TVShowEpisode, TVShowEpisodeInDB, TVShowInDB
from fsubs.models.video import VideoInstanceInDB

LOGGER = logging.getLogger(__name__)
router = APIRouter()

client = MongoClient(
    host=config["db"]["hostname"],
    port=config["db"].getint("port"),
    username='root',
    password='example',
)

TV_SHOW_DAO = TVShowDAO(client=client)

# /tv_shows endpoints


@router.post("", tags=['tv shows'], response_model=ObjectIdStr, status_code=201)
async def create_tv_show(tv_show: TVShow):
    """
    Create a tv show.

    **tv_show** - The tv show data to create the tv show with.

    **returns** - The id of the newly created tv show.
    """
    raise NotImplementedError


@router.get("/{uri}", response_model=TVShowInDB, tags=['tv shows'])
async def get_tv_show(uri: ObjectIdStr):
    """
    Get a tv show.

    **param uri** - The uri of the tv show to get.

    **returns** - The tv show data.
    """
    raise NotImplementedError


@router.get("", response_model=List[TVShowInDB], tags=['tv shows'])
async def get_tv_shows(start: int = Query(0, ge=0), page_length: int = Query(100, ge=1)):
    """
    Get tv shows.

    **param start** - The starting position to start getting tv shows at.

    **param page_length** - The number of tv shows to get.

    **returns** A list of tv shows.
    """
    raise NotImplementedError


@router.put("/{uri}", tags=['tv shows'], response_model=TVShowInDB, status_code=201)
async def update_tv_show(uri: ObjectIdStr, tv_show: TVShow):
    """
    Update a tv show.

    **uri** - The uri of the tv show to update.

    **tv_show** - The tv data to update tv show with.

    **returns** - The new tv show data.
    """
    raise NotImplementedError


@router.delete("/{uri}", tags=['tv shows'], status_code=204)
async def delete_tv_show(uri: ObjectIdStr):
    """
    Delete a tv show.

    This will also delete any associated tv episodes.

    **uri** - The uri of the tv show to delete.

    **returns** - No content.
    """
    raise NotImplementedError


#  /tv_shows/episodes endpoints

@router.post("/{uri}/episodes", tags=['tv show episodes'], response_model=str, status_code=201)
async def create_tv_show_episode(uri: ObjectIdStr, episode: TVShowEpisode):
    """
    Create a tv show episode.

    **uri** - The uri of the tv show to attach the tv episode to.

    **episode** - The tv show episode data to create the tv show episode with.

    **returns** - The id of the newly created tv show episode.
    """
    raise NotImplementedError


@router.get("/episodes/{uri}", response_model=TVShowEpisodeInDB, tags=['tv show episodes'])
async def get_tv_show_episode(uri: ObjectIdStr):
    """
    Get a tv show episode.

    **param uri** - The uri of the tv show episode to get.

    **returns** - The tv show episode data.
    """
    raise NotImplementedError


@router.get("/{uri}/episodes", response_model=List[TVShowEpisodeInDB], tags=['tv show episodes'])
async def get_tv_show_episodes(uri: ObjectIdStr):
    """
    Get **all** tv show episodes.

    **uri** - The uri of the tv show to get episodes for.

    **returns** - A list of tv show episodes.
    """
    raise NotImplementedError


@router.put(
    "/episodes/{uri}",
    tags=['tv show episodes'],
    response_model=TVShowEpisodeInDB,
    status_code=201)
async def update_tv_show_episode(uri: ObjectIdStr, episode: TVShowEpisode):
    """
    Update a tv show episode.

    **uri** - The uri of the tv show episode to update.

    **episode** - The tv episode data to update the tv show episode with.

    **returns** - The new tv show episode data.
    """
    raise NotImplementedError


@router.delete("/episodes/{uri}", tags=['tv show episodes'], status_code=204)
async def delete_tv_show_episode(uri: ObjectIdStr):
    """
    Delete a tv show episode.

    This will also delete any tv show episode versions.

    **uri** - The uri of the tv show episode to delete.

    **returns** - No content.
    """
    raise NotImplementedError


#  /tv_shows/episodes/versions endpoints

@router.post(
    "/episodes/{uri}/versions",
    tags=['tv episode versions'],
    response_model=ObjectIdStr,
    status_code=201)
async def create_tv_show_episode_version(episode_version: VideoInstanceInDB):
    """
    Create a tv show episode version.

    **episode_version** - The tv show episode version data to create the tv show episode
    version with.

    **returns** - The id of the newly created tv show episode version.
    """
    raise NotImplementedError


@router.get(
    "/episodes/versions/{uri}",
    response_model=VideoInstanceInDB,
    tags=['tv episode versions'])
async def get_tv_show_episode_version(uri: ObjectIdStr):
    """
    Get a tv show episode version.

    **param uri** - The uri of the tv show episode version to get.

    **returns** - The tv show episode version data.
    """
    raise NotImplementedError


@router.get(
    "/episodes/{uri}/versions",
    response_model=List[VideoInstanceInDB],
    tags=['tv episode versions'])
async def get_tv_show_episode_versions(uri: ObjectIdStr):
    """
    Get **all** the versions for a tv show episode.

    **uri** - The uri of the episode to get episode versions for.

    **returns** - A list of tv show episode versions.
    """
    raise NotImplementedError


@router.put(
    "/episodes/versions/{uri}",
    tags=['tv episode versions'],
    response_model=VideoInstanceInDB,
    status_code=201)
async def update_tv_show_episode_version(uri: ObjectIdStr, episode: VideoInstanceInDB):
    """
    Update a tv show episode version.

    **uri** - The uri of the tv show episode version to update.

    **episode** - The tv episode version data to update the tv show episode with.
    """
    raise NotImplementedError


@router.delete("/episodes/versions/{uri}", tags=['tv episode versions'], status_code=204)
async def delete_tv_show_episode_version(uri: ObjectIdStr):
    """
    Delete a tv show episode verion.

    **uri** - The uri of the tv show episode to delete.

    **returns** - No content.
    """
    raise NotImplementedError


@router.delete("/episodes/{uri}/versions", tags=['tv episode versions'], status_code=204)
async def delete_tv_show_episode_versions(uri: ObjectIdStr):
    """
    Delete **all** episode versions for a tv show episode.

    **uri** - The uri of the tv show episode to delete all versions for.

    **returns** - No content.
    """
    raise NotImplementedError
