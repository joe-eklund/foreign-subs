"""REST API functions."""
from datetime import datetime, timezone

import addict as ad
from fastapi import FastAPI
from pymongo import MongoClient

from crud.movie import MovieDAO
from models.video import VideoBase

app = FastAPI()

MOVIE_DAO = MovieDAO(client=MongoClient('localhost', 27017, username='root', password='example'))

# GET
# returns VideoBase including list of VideoInstances
@app.get("/movies/{uri}")
async def get_movie(uri):
    """Get a movie."""
    raise NotImplementedError

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

# DELETE
