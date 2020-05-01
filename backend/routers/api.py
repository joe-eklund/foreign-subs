"""REST API functions."""
from datetime import datetime, timezone

import addict as ad
from fastapi import FastAPI
from pymongo import MongoClient

from crud.movie import MovieDAO
from models.video import VideoBase

app = FastAPI()

MOVIE_DAO = MovieDAO(client=MongoClient('localhost', 27017, username='root', password='example'))


@app.get("/movies/{uri}")
async def get_movie(uri: str):
    """
    Get a movie.

    :param uri: The uri of the movie to get.
    """
    return MOVIE_DAO.read(movie_id=uri)

# GET movie instance
@app.get("/movies/{uri}/versions/{v_uri}", status_code=405)
async def get_movie_version(uri: str, v_uri: str):
    """
    Get a movie version.

    :param uri: The uri of the base movie to use.
    :param v_uri: The uri of the version of the movie to get.
    """
    return "Not implemented yet."

# POST
@app.post("/movies", response_model=str, status_code=201)
async def create_movie(movie: VideoBase):
    """Create a movie."""
    user = 'admin'  # change to real user with auth later
    movie_to_store = ad.Dict(movie.dict())

    # Set metadata
    movie_to_store.Metadata.date_created = datetime.now(timezone.utc)
    movie_to_store.Metadata.created_by = user
    movie_to_store.Metadata.last_modified = datetime.now(timezone.utc)
    movie_to_store.Metadata.modified_by = user
    return str(MOVIE_DAO.create(movie=movie_to_store.to_dict()))

# PUT
@app.put("/movies", response_model=str, status_code=201)
async def update_movie(uri: str, movie: VideoBase):
    """Update a movie."""
    user = 'admin'  # change to real user with auth later
    movie_to_store = ad.Dict(movie.dict())

    # Set metadata
    movie_to_store.Metadata.last_modified = datetime.now(timezone.utc)
    movie_to_store.Metadata.modified_by = user
    return str(MOVIE_DAO.update(movie_id=uri, movie=movie_to_store.to_dict()))


# DELETE
