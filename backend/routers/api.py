"""REST API functions."""

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
async def create_movie(video_base: VideoBase):
    """Create a movie."""
    return str(MOVIE_DAO.create(movie=video_base))

# PUT

# DELETE
