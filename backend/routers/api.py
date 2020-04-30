"""REST API functions."""

from fastapi import FastAPI

app = FastAPI()

# GET
# returns VideoBase including list of VideoInstances
@app.get("/movies/{uri}")
async def get_movie(uri):
    raise NotImplementedError

# POST

# PUT

# DELETE
