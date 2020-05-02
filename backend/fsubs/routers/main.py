"""Setup FastAPI."""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fsubs.routers import movies

LOGGER = logging.getLogger(__name__)

origins = [
    "http://localhost:4200",
]

openapi_prefix = ''  # Set me to run swagger ot a base url

LOGGER.info(f'Building FastAPI app with base url: <{openapi_prefix}>.')
app = FastAPI(openapi_prefix=openapi_prefix)

LOGGER.info('Setting up FastAPI middleware.')
LOGGER.debug(f'Using origins: <{origins}>.')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOGGER.info('Loading routers.')
app.include_router(movies.router, prefix="/movies")
