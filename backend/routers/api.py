"""REST API functions."""

from fastapi import FastAPI

from models.video import VideoBase, VideoBaseResponse

app = FastAPI()

# GET
# returns VideoBase including list of VideoInstances
@app.get("/movies/{uri}")
async def get_movie(uri):
    raise NotImplementedError

# POST
@app.post("/movies", response_model=VideoBaseResponse, status_code=201)
async def create_movie(video_base: VideoBase):
    """Create a movie."""
    return video_base

# PUT

# DELETE
