"""REST API functions."""
from datetime import datetime, timezone

import addict as ad
from fastapi import FastAPI
from pymongo import MongoClient

from backend.config.config import config
from backend.crud.movie import MovieDAO
from backend.models.video import VideoBase, VideoInstance

app = FastAPI()

client = MongoClient(
    host=config["db"]["hostname"],
    port=config["db"].getint("port"),
    username='root',
    password='example',
)

MOVIE_DAO = MovieDAO(client=client)


# /movies endpoints

@app.post("/movies", tags=['movies'], response_model=str, status_code=201)
async def create_movie(movie: VideoBase):
    """
    Create a movie.

    **movie** - The movie data to create the movie with.
    """
    user = 'admin'  # change to real user with auth later
    movie_to_store = ad.Dict(movie.dict())

    # Set metadata
    movie_to_store.Metadata.date_created = datetime.now(timezone.utc)
    movie_to_store.Metadata.created_by = user
    movie_to_store.Metadata.last_modified = datetime.now(timezone.utc)
    movie_to_store.Metadata.modified_by = user
    return str(MOVIE_DAO.create(movie=movie_to_store.to_dict()))


@app.get("/movies/{uri}", tags=['movies'])
async def get_movie(uri: str):
    """
    Get a movie.

    **param uri** - The uri of the movie to get.
    """
    return MOVIE_DAO.read(movie_id=uri)


@app.get("/movies", tags=['movies'])
async def get_movies(start: int = 0, page_length: int = 2):
    """
    Get movies.

    **param start** - The starting position to start getting movies at.
    **param page_length** - The number of movies to get.
    """
    return MOVIE_DAO.read_multi(page_length=page_length)


@app.put("/movies/{uri}", tags=['movies'], response_model=str, status_code=201)
async def update_movie(uri: str, movie: VideoBase):
    """
    Update a movie.

    **uri** - The uri of the movie to update.

    **movie** - The movie data to update the movie with.
    """
    user = 'admin'  # change to real user with auth later
    movie_to_store = ad.Dict(movie.dict())

    # Set metadata
    movie_to_store.Metadata.last_modified = datetime.now(timezone.utc)
    movie_to_store.Metadata.modified_by = user
    return str(MOVIE_DAO.update(movie_id=uri, movie=movie_to_store.to_dict()))


@app.delete("/movies/{uri}", tags=['movies'], status_code=204)
async def delete_movie(uri: str):
    """
    Delete a movie.

    **uri** - The uri of the movie to delete.
    """
    return MOVIE_DAO.delete(movie_id=uri)


# /movies/versions endpoints

@app.post("/movies/{uri}/versions", tags=['movie versions'], status_code=405)
async def create_movie_version(uri: str, movie_version: VideoInstance):
    """
    Create a new movie version.

    **uri** - The uri of the movie to attach the movie version to.

    **movie_version** - The movie version data to create the movie version with.
    """
    return "Not implemented yet."


@app.get("/movies/versions/{uri}", tags=['movie versions'], status_code=405)
async def get_movie_version(uri: str):
    """
    Get a movie version.

    **uri** - The uri of the version of the movie to get.
    """
    return "Not implemented yet."


@app.put("/movies/versions/{uri}", tags=['movie versions'], status_code=405)
async def update_movie_version(uri: str, movie_version: VideoInstance):
    """
    Update a movie version.

    **uri** - The uri of the movie version of to update.

    **movie_version** - The movie version data to update the movie version with.
    """
    return "Not implemented yet."


@app.delete("/movies/versions/{uri}", tags=['movie versions'], status_code=405)
async def delete_movie_version(uri: str):
    """
    Delete a movie version.

    **uri** - The uri of the movie version to delete.
    """
    return "Not implemented yet."
