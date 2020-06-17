"""REST API tv show functions."""

import logging
from datetime import datetime, timezone
from typing import List

import addict as ad
from fastapi import APIRouter, HTTPException, Query
from pymongo import MongoClient

from fsubs.config.config import Config
from fsubs.crud.tvshow import TVShowDAO
from fsubs.models.misc import ObjectIdStr
from fsubs.models.tvshow import TVShowEpisode, TVShowEpisodeInDB, TVShowInDB
from fsubs.models.video import VideoBase, VideoBaseInDB, VideoInstanceInDB

LOGGER = logging.getLogger(__name__)
router = APIRouter()
config = Config()

client = MongoClient(
    host=config["db"]["hostname"],
    port=config["db"].getint("port"),
    username='root',
    password='example',
)

TV_SHOW_DAO = TVShowDAO(client=client)

# /tv_shows endpoints


@router.post("", tags=['tv shows'], response_model=ObjectIdStr, status_code=201)
async def create_tv_show(tv_show: VideoBase):
    """
    Create a tv show.

    **tv_show** - The tv show data to create the tv show with.

    **returns** - The id of the newly created tv show.
    """
    user = 'admin'  # change to real user with auth later
    LOGGER.debug(f'Creating tv show: <{tv_show}> as user: <{user}>.')
    tv_show_to_store = ad.Dict(tv_show.dict())

    # Set metadata
    tv_show_to_store.metadata.date_created = datetime.now(timezone.utc)
    tv_show_to_store.metadata.created_by = user
    tv_show_to_store.metadata.last_modified = datetime.now(timezone.utc)
    tv_show_to_store.metadata.modified_by = user
    return str(TV_SHOW_DAO.create(tv_show=tv_show_to_store.to_dict()))


@router.get("/{uri}", response_model=VideoBaseInDB, tags=['tv shows'])
async def get_tv_show(uri: ObjectIdStr):
    """
    Get a tv show.

    **param uri** - The uri of the tv show to get.

    **returns** - The tv show data.
    """
    LOGGER.debug(f'Getting tv show: {uri}.')
    tv_show = TV_SHOW_DAO.read(tv_show_id=uri)
    if not tv_show:
        raise HTTPException(status_code=404, detail="TV show not found.")
    return tv_show


@router.get("", response_model=List[VideoBaseInDB], tags=['tv shows'])
async def get_tv_shows(start: int = Query(0, ge=0), page_length: int = Query(100, ge=1)):
    """
    Get tv shows.

    **param start** - The starting position to start getting tv shows at.

    **param page_length** - The number of tv shows to get.

    **returns** A list of tv shows.
    """
    LOGGER.debug(f'Getting tv shows with start: <{start}> and page_length: <{page_length}>.')
    return TV_SHOW_DAO.read_multi(limit=page_length, skip=start)


@router.put("/{uri}", tags=['tv shows'], response_model=TVShowInDB, status_code=201)
async def update_tv_show(uri: ObjectIdStr, tv_show: VideoBase):
    """
    Update a tv show.

    **uri** - The uri of the tv show to update.

    **tv_show** - The tv data to update tv show with.

    **returns** - The new tv show data.
    """
    user = 'admin'  # change to real user with auth later
    LOGGER.debug(f'Updating tv_show: <{uri}> with data: <{tv_show}> and user: <{user}>.')
    tv_show_to_store = ad.Dict(tv_show.dict())

    # Set metadata
    old_tv_show = ad.Dict(TV_SHOW_DAO.read(tv_show_id=uri))
    if not old_tv_show:
        LOGGER.debug(f'TV show not found for: {uri}.')
        raise HTTPException(status_code=404, detail="TV show not found.")

    tv_show_to_store.metadata.date_created = old_tv_show.metadata.date_created
    tv_show_to_store.metadata.created_by = old_tv_show.metadata.created_by
    tv_show_to_store.metadata.last_modified = datetime.now(timezone.utc)
    tv_show_to_store.metadata.modified_by = user

    TV_SHOW_DAO.update(tv_show_id=uri, tv_show=tv_show_to_store.to_dict())

    tv_show_to_store.id = uri
    return tv_show_to_store


@router.delete("/{uri}", tags=['tv shows'], status_code=204)
async def delete_tv_show(uri: ObjectIdStr):
    """
    Delete a tv show.

    This will also delete any associated tv episodes.

    **uri** - The uri of the tv show to delete.

    **returns** - No content.
    """
    LOGGER.debug(f'Deleting tv show: <{uri}>.')
    TV_SHOW_DAO.delete(tv_show_id=uri)
    # TODO delete episodes

#  /tv_shows/episodes endpoints


@router.post("/{uri}/episodes", tags=['tv show episodes'], response_model=str, status_code=201)
async def create_tv_show_episode(uri: ObjectIdStr, episode: VideoBase):
    """
    Create a tv show episode.

    **uri** - The uri of the tv show to attach the tv episode to.

    **episode** - The tv show episode data to create the tv show episode with.

    **returns** - The id of the newly created tv show episode.
    """
    # Make sure tv show exists
    tv_show = TV_SHOW_DAO.read(tv_show_id=uri)
    if not tv_show:
        raise HTTPException(status_code=422, detail='uri must be a valid tv show id.')
    user = 'admin'  # change to real user with auth later
    LOGGER.debug(f'Creating tv episode for tv show: <{uri}> with data: <{episode}> and '
                 f'user: <{user}>.')
    episode_to_store = ad.Dict(episode.dict())

    # Set metadata
    episode_to_store.video_base_id = uri
    episode_to_store.metadata.date_created = datetime.now(timezone.utc)
    episode_to_store.metadata.created_by = user
    episode_to_store.metadata.last_modified = datetime.now(timezone.utc)
    episode_to_store.metadata.modified_by = user

    return str(TV_SHOW_DAO.create_episode(episode=episode_to_store.to_dict()))


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
