"""REST API movie functions."""
import logging
from datetime import datetime, timezone
from typing import List


import addict as ad
from fastapi import APIRouter, Depends, Query, HTTPException
from pymongo import MongoClient

from fsubs.config.config import Config
from fsubs.crud.movie import MovieDAO
from fsubs.models.misc import ObjectIdStr
from fsubs.models.video import VideoBase, VideoBaseInDB, VideoInstance, VideoInstanceInDB
from fsubs.routers.authenticate import get_token_header

LOGGER = logging.getLogger(__name__)
router = APIRouter()
config = Config()

client = MongoClient(
    host=config["db"]["hostname"],
    port=config["db"].getint("port"),
    username='root',
    password='example',
)

MOVIE_DAO = MovieDAO(client=client)

# /movies endpoints


@router.post("", tags=['movies'], response_model=ObjectIdStr, status_code=201)
async def create_movie(movie: VideoBase, username: str = Depends(get_token_header)):
    """
    Create a movie.

    **movie** - The movie data to create the movie with.

    **returns** - The id of the newly created movie.
    """
    user = username  # change to real user with auth later
    LOGGER.debug(f'Creating movie: <{movie}> as user: <{user}>.')
    movie_to_store = ad.Dict(movie.dict())

    # Set metadata
    movie_to_store.metadata.date_created = datetime.now(timezone.utc)
    movie_to_store.metadata.created_by = user
    movie_to_store.metadata.last_modified = datetime.now(timezone.utc)
    movie_to_store.metadata.modified_by = user
    return str(MOVIE_DAO.create(movie=movie_to_store.to_dict()))


@router.get("/{uri}", response_model=VideoBaseInDB, tags=['movies'])
async def get_movie(uri: ObjectIdStr):
    """
    Get a movie.

    **param uri** - The uri of the movie to get.

    **returns** - The movie data.
    """
    LOGGER.debug(f'Getting movie: {uri}.')
    movie = MOVIE_DAO.read(movie_id=uri)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")
    return movie


@router.get("", response_model=List[VideoBaseInDB], tags=['movies'])
async def get_movies(start: int = Query(0, ge=0), page_length: int = Query(100, ge=1)):
    """
    Get movies.

    **param start** - The starting position to start getting movies at.

    **param page_length** - The number of movies to get.

    **returns** - A list of movies.
    """
    LOGGER.debug(f'Getting movies with start: <{start}> and page_length: <{page_length}>.')
    return MOVIE_DAO.read_multi(limit=page_length, skip=start)


@router.put("/{uri}", tags=['movies'], response_model=VideoBaseInDB, status_code=201)
async def update_movie(uri: ObjectIdStr, movie: VideoBase):
    """
    Update a movie.

    **uri** - The uri of the movie to update.

    **movie** - The movie data to update the movie with.

    **returns** - The new movie data.
    """
    user = 'admin'  # change to real user with auth later
    LOGGER.debug(f'Updating movie: <{uri}> with data: <{movie}> and user: <{user}>.')
    movie_to_store = ad.Dict(movie.dict())

    # Set metadata
    old_movie = ad.Dict(MOVIE_DAO.read(movie_id=uri))
    if not old_movie:
        LOGGER.debug(f'Movie not found for: {uri}.')
        raise HTTPException(status_code=404, detail="Movie not found.")

    movie_to_store.metadata.date_created = old_movie.metadata.date_created
    movie_to_store.metadata.created_by = old_movie.metadata.created_by
    movie_to_store.metadata.last_modified = datetime.now(timezone.utc)
    movie_to_store.metadata.modified_by = user

    MOVIE_DAO.update(movie_id=uri, movie=movie_to_store.to_dict())

    movie_to_store.id = uri
    return movie_to_store


@router.delete("/{uri}", tags=['movies'], status_code=204)
async def delete_movie(uri: ObjectIdStr):
    """
    Delete a movie.

    This will also delete any associated movie versions.

    **uri** - The uri of the movie to delete.

    **returns** - No content.
    """
    LOGGER.debug(f'Deleting movie: <{uri}>.')
    MOVIE_DAO.delete(movie_id=uri)
    MOVIE_DAO.delete_movie_versions(movie_id=uri)


# /movies/versions endpoints

@router.post(
    "/{uri}/versions",
    response_model=ObjectIdStr,
    tags=['movie versions'],
    status_code=201)
async def create_movie_version(uri: ObjectIdStr, movie_version: VideoInstance):
    """
    Create a new movie version.

    **uri** - The uri of the movie to attach the movie version to.

    **movie_version** - The movie version data to create the movie version with.

    **returns** - The id of the newly created movie version.
    """
    # Make sure movie exists
    movie = MOVIE_DAO.read(movie_id=uri)
    if not movie:
        raise HTTPException(status_code=422, detail='uri must be valid movie id.')
    user = 'admin'  # change to real user with auth later
    LOGGER.debug(f'Creating movie version for movie: <{uri}> with data: <{movie_version}> and '
                 f'user: <{user}>.')
    movie_version_to_store = ad.Dict(movie_version.dict())

    # Set metadata
    movie_version_to_store.video_base_id = uri
    movie_version_to_store.metadata.date_created = datetime.now(timezone.utc)
    movie_version_to_store.metadata.created_by = user
    movie_version_to_store.metadata.last_modified = datetime.now(timezone.utc)
    movie_version_to_store.metadata.modified_by = user

    return str(MOVIE_DAO.create_version(movie_version=movie_version_to_store.to_dict()))


@router.get("/versions/{uri}", 
            response_model=VideoInstanceInDB,
            tags=['movie versions'],
            status_code=200)
async def get_movie_version(uri: ObjectIdStr):
    """
    Get a movie version.

    **uri** - The uri of the version of the movie to get.

    **returns** - The movie version data.
    """
    LOGGER.debug(f'Getting movie version: <{uri}>.')
    movie_version = MOVIE_DAO.read_version(movie_version_id=uri)
    if not movie_version:
        raise HTTPException(status_code=404, detail="Movie version not found.")
    return movie_version


@router.get("/{uri}/versions",
            response_model=List[VideoInstanceInDB],
            tags=['movie versions'],
            status_code=200)
async def get_movie_versions(uri: ObjectIdStr):
    """
    Get **all** of the versions for a movie.

    **uri** - The uri of movie to get all versions.

    **returns** - A list of movie versions.
    """
    LOGGER.debug(f'Getting movie versions for movie: {uri}.')
    movie_versions = MOVIE_DAO.read_movie_versions(movie_id=uri)
    return movie_versions


@router.delete("/{uri}/versions", tags=['movie versions'], status_code=204)
async def delete_movie_versions(uri: ObjectIdStr):
    """
    Delete **all** movie versions for a movie.

    **uri** - The uri of the movie to delete all versions for.

    **returns** - No content.
    """
    LOGGER.debug(f'Deleting movie versions for movie: <{uri}>.')
    MOVIE_DAO.delete_movie_versions(movie_id=uri)


@router.put("/versions/{uri}",
            response_model=VideoInstanceInDB,
            tags=['movie versions'],
            status_code=201)
async def update_movie_version(uri: ObjectIdStr, movie_version: VideoInstance):
    """
    Update a movie version.

    **uri** - The uri of the movie version of to update.

    **movie_version** - The movie version data to update the movie version with.

    **returns** - The new movie version data.
    """
    user = 'admin'  # change to real user with auth later
    LOGGER.debug(f'Updating movie version uri: <{uri}> with movie_version: <{movie_version}> and '
                 f'user: <{user}>.')

    movie_version_to_store = ad.Dict(movie_version.dict())

    # Set metadata
    old_movie_version = ad.Dict(MOVIE_DAO.read_version(movie_version_id=uri))

    movie_version_to_store.metadata.date_created = old_movie_version.metadata.date_created
    movie_version_to_store.metadata.created_by = old_movie_version.metadata.created_by
    movie_version_to_store.metadata.last_modified = datetime.now(timezone.utc)
    movie_version_to_store.metadata.modified_by = user

    MOVIE_DAO.update_version(movie_version_id=uri, movie_version=movie_version_to_store.to_dict())

    updated_movie = MOVIE_DAO.read_version(movie_version_id=uri)
    if not updated_movie:
        msg = "Something went wrong while trying to update the movie version: {uri}."
        LOGGER.error(msg)
        raise HTTPException(
            status_code=500,
            detail=msg)
    return updated_movie

@router.delete("/versions/{uri}", tags=['movie versions'], status_code=204)
async def delete_movie_version(uri: ObjectIdStr):
    """
    Delete a movie version.

    **uri** - The uri of the movie version to delete.

    **returns** - No content.
    """
    LOGGER.debug(f'Deleting movie version: <{uri}>.')
    MOVIE_DAO.delete_version(movie_version_id=uri)
