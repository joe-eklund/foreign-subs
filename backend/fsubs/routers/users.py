"""REST API user functions."""
import logging
from datetime import datetime, timezone

import addict as ad
from fastapi import APIRouter
from pymongo import MongoClient

from fsubs.config.config import Config
from fsubs.crud.user import UserDAO
from fsubs.models.misc import ObjectIdStr
from fsubs.models.user import UserCreate

LOGGER = logging.getLogger(__name__)
router = APIRouter()
config = Config()

client = MongoClient(
    host=config["db"]["hostname"],
    port=config["db"].getint("port"),
    username='root',
    password='example',
)

USER_DAO = UserDAO(client=client)

# / user endpoints


@router.post("", tags=['users'], response_model=ObjectIdStr, status_code=201)
async def create_user(user_to_create: UserCreate):
    """
    Create a user.

    **user_to_create** - The user data to create the user with.

    **returns** - The id of the newly created user.
    """
    user = 'admin'  # change to real user with auth later
    LOGGER.debug('Creating user with username: {user.username}, email: {user.email}, '
                 'access: {user.access}.')
    user_to_store = ad.Dict(user_to_create.dict())
    # set metadata
    LOGGER.debug('Setting metadata.')
    user_to_store.metadata.date_created = datetime.now(timezone.utc)
    user_to_store.metadata.created_by = user
    user_to_store.metadata.last_modified = datetime.now(timezone.utc)
    user_to_store.metadata.modified_by = user
    return str(USER_DAO.create(user=user_to_store))
