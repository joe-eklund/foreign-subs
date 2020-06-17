"""REST API user functions."""
import logging
from datetime import datetime, timezone
from typing import List

import addict as ad
from fastapi import APIRouter, Depends, Query, HTTPException
from pymongo import MongoClient

from fsubs.config.config import Config
from fsubs.crud.user import UserDAO
from fsubs.models.misc import ObjectIdStr
from fsubs.models.user import Access, UserRead, UserCreate, UserCreateToDAO
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


@router.get(
    '',
    tags=['users'],
    response_model=List[UserRead],
    status_code=200)
async def read_users(
        start: int = Query(0, ge=0),
        page_length: int = Query(100, ge=1),
        username: str = Depends(get_token_header)):
    """
    Get users.

    A user must have admin access to read other users.

    **param start** - The starting position to start getting users at.

    **param page_length** - The number of users to get.

    **returns** - A list of users.
    """
    LOGGER.debug(f'Getting users with start: <{start}> and page_length: <{page_length}.')
    user = ad.Dict(USER_DAO.read_by_username(username=username))
    if not user:
        raise HTTPException(
            status_code=500,
            detail=f'Unable to get user data for: {username}. Cannot proceed with reading '
                   f'of users.')
    if user.access == Access['admin']:
        return USER_DAO.read_multi(limit=page_length, skip=start)
    raise HTTPException(status_code=403, detail='User does not have access to read other users.')


@router.get(
    '/self',
    tags=['users'],
    response_model=UserRead,
    status_code=200)
async def read_self(username: str = Depends(get_token_header)):
    """
    Get the currently logged in user.

    **returns** - The user data.
    """
    LOGGER.debug(f'Getting user: {username}.')
    user = USER_DAO.read_by_username(username=username)
    if not user:
        raise HTTPException(status_code=500, detail='Unable to get user data for: {username}.')
    return user


@router.get(
    '/{username}',
    tags=['users'],
    response_model=UserRead,
    status_code=200)
async def read_user(username: str, acting_username: str = Depends(get_token_header)):
    """
    Get the given user.

    A user must have admin access to read other users.

    **returns** - The user data.
    """
    LOGGER.debug(f'Getting user: {username}.')
    acting_user = ad.Dict(USER_DAO.read_by_username(username=acting_username))
    if not acting_user:
        raise HTTPException(
            status_code=500,
            detail=f'Unable to get user data for: {acting_username}. Cannot proceed with reading '
                   f'of {username}.')
    if acting_user.access == Access['admin'] or acting_username == username:
        user = ad.Dict(USER_DAO.read_by_username(username=username))
        if not user:
            raise HTTPException(status_code=404, detail=f'Unable to find user {username}.')
        return user
    raise HTTPException(status_code=403, detail='User does not have access to read other users.')


@router.post(
    '',
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
