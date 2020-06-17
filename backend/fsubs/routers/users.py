"""REST API user functions."""
import logging
from datetime import datetime, timezone

import addict as ad
from fastapi import APIRouter, Depends, HTTPException
from pymongo import MongoClient

from fsubs.config.config import Config
from fsubs.crud.user import UserDAO
from fsubs.models.misc import ObjectIdStr
from fsubs.models.user import Access, UserCreate, UserCreateToDAO, UserInDB
from fsubs.routers.authenticate import get_token_header
from fsubs.utils import users as user_utils

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


@router.post(
    "",
    tags=['users'],
    response_model=ObjectIdStr,
    status_code=201)
async def create_user(user_to_create: UserCreate):
    """
    Create a user.

    **user_to_create** - The user data to create the user with.

    **returns** - The id of the newly created user.
    """
    user = ad.Dict(user_to_create.dict())
    LOGGER.info(f'Creating user with username: {user.username}, email: {user.email}.')

    # Check if username or email is in use
    if USER_DAO.read_by_username(username=user.username):
        raise HTTPException(status_code=409, detail='That username is already in use.')
    if USER_DAO.read_by_email(email=user.email):
        raise HTTPException(status_code=409, detail='That email is already in use.')

    # set metadata
    LOGGER.debug('Setting metadata.')
    user.metadata.date_created = datetime.now(timezone.utc)
    user.metadata.created_by = user.username
    user.metadata.last_modified = datetime.now(timezone.utc)
    user.metadata.modified_by = user.username

    # hash password
    salt, key = user_utils.hash_password(password=user.password)
    user.salt = salt
    user.hashed_password = key
    user_to_store = UserCreateToDAO(**user)
    LOGGER.debug(f'User to store is: {user_to_store}')
    return str(USER_DAO.create(user=user_to_store))
