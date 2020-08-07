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
from fsubs.models.user import Access, UserRead, UserCreate, UserCreateToDAO, UserUpdate, UserPatch
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
    user = ad.Dict(await USER_DAO.read_by_username(username=username))
    if not user:
        raise HTTPException(
            status_code=500,
            detail=f'Unable to get user data for: {username}. Cannot proceed with reading '
                   f'of users.')
    if not user.access == Access['admin']:
        raise HTTPException(
            status_code=403,
            detail='User does not have access to read other users.')
    return await USER_DAO.read_multi(limit=page_length, skip=start)


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
    user = await USER_DAO.read_by_username(username=username)
    if not user:
        raise HTTPException(status_code=500, detail='Unable to get user data for: {username}.')
    return user


@router.get(
    '/username/{username}',
    tags=['users'],
    response_model=UserRead,
    status_code=200)
async def read_user(username: str, acting_username: str = Depends(get_token_header)):
    """
    Get the given user.

    A user must have admin access to read other users.

    **username** - The username of the user to read.

    **returns** - The user data.
    """
    LOGGER.debug(f'Getting user: {username}.')
    acting_user = ad.Dict(await USER_DAO.read_by_username(username=acting_username))
    if not acting_user:
        raise HTTPException(
            status_code=500,
            detail=f'Unable to get user data for: {acting_username}. Cannot proceed with reading '
                   f'of {username}.')
    if not acting_user.access == Access['admin'] and acting_username != username:
        raise HTTPException(
            status_code=403,
            detail='User does not have access to read other users.')
    user = ad.Dict(await USER_DAO.read_by_username(username=username))
    if not user:
        raise HTTPException(status_code=404, detail=f'Unable to find user {username}.')
    return user


@router.get(
    '/userid/{user_id}',
    tags=['users'],
    response_model=UserRead,
    status_code=200)
async def read_user_id(user_id: ObjectIdStr, acting_username: str = Depends(get_token_header)):
    """
    Get the given user.

    A user must have admin access to read other users.

    **user_id** - The id of the user to read.

    **returns** - The user data.
    """
    LOGGER.debug(f'Getting user id: {user_id}.')
    acting_user = ad.Dict(await USER_DAO.read_by_username(username=acting_username))
    if not acting_user:
        raise HTTPException(
            status_code=500,
            detail=f'Unable to get user data for: {acting_username}. Cannot proceed with reading '
                   f'of {user_id}.')
    if not acting_user.access == Access['admin'] and acting_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail='User does not have access to read other users.')
    user = ad.Dict(await USER_DAO.read(user_id=user_id))
    if not user:
        raise HTTPException(status_code=404, detail=f'Unable to find user {user_id}.')
    return user


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
    if await USER_DAO.read_by_username(username=user.username):
        raise HTTPException(status_code=409, detail='That username is already in use.')
    if await USER_DAO.read_by_email(email=user.email):
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
    return str(await USER_DAO.create(user=user_to_store))


@router.put(
    '/userid/{user_id}',
    tags=['users'],
    response_model=UserRead,
    status_code=201)
async def update_user(
        user_id: ObjectIdStr,
        user_to_update: UserUpdate,
        acting_username: str = Depends(get_token_header)):
    """
    Update a given user with the given data.

    A user must have admin access to update other users.

    **user_to_update** - The user data to update the user with.

    **returns** - The user data.
    """
    LOGGER.debug(f'Updating user id: {user_id}.')
    acting_user = ad.Dict(await USER_DAO.read_by_username(username=acting_username))
    if not acting_user:
        raise HTTPException(
            status_code=500,
            detail=f'Unable to get user data for: {acting_username}. Cannot proceed with updating '
                   f'of {user_id}.')
    if not acting_user.access == Access['admin'] and acting_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail='User does not have access to update other users.')

    old_user = ad.Dict(await USER_DAO.read(user_id=user_id))
    if not old_user:
        raise HTTPException(status_code=404, detail=f'Unable to find user {user_id}.')

    # Check if new email is in use.
    users = await USER_DAO.read_multi(search={'email': user_to_update.email})
    if len(users) > 0 and users[0]['id'] != user_id:
        raise HTTPException(
            status_code=422,
            detail=f'Unable to update user {old_user.username} {user_id} to email: '
                   '{user_to_update.email} because that email is already in use.')

    user = ad.Dict(user_to_update.dict())
    # set info that cannot be changed from user
    LOGGER.debug('Setting metadata and unchangable data.')
    user.username = old_user.username
    user.metadata.date_created = old_user.metadata.date_created
    user.metadata.created_by = old_user.metadata.created_by
    user.metadata.last_modified = datetime.now(timezone.utc)
    user.metadata.modified_by = acting_username
    user.verified = False  # reset because they are setting a new email that must be verified
    user.access = old_user.access

    # hash new password
    salt, key = user_utils.hash_password(password=user_to_update.password)
    user.salt = salt
    user.hashed_password = key
    user_to_store = UserCreateToDAO(**user)
    LOGGER.debug(f'User to store is: {user_to_store}')

    await USER_DAO.update(user_id=user_id, user=user_to_store.dict())
    return await USER_DAO.read(user_id=user_id)


@router.patch(
    '/userid/{user_id}',
    tags=['users'],
    response_model=UserRead,
    status_code=201)
async def patch_user(
        user_id: ObjectIdStr,
        user_to_patch: UserPatch,
        acting_username: str = Depends(get_token_header)):
    """
    Patch a given user with the given data.

    A user must have admin access to patch other users.

    **user_to_patch** - The user data to patch the user with.

    **returns** - The user data.
    """
    LOGGER.debug(f'Patching user id: {user_id}.')
    acting_user = ad.Dict(await USER_DAO.read_by_username(username=acting_username))
    if not acting_user:
        raise HTTPException(
            status_code=500,
            detail=f'Unable to get user data for: {acting_username}. Cannot proceed with patching '
                   f'of {user_id}.')
    if not acting_user.access == Access['admin'] and acting_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail='User does not have access to patch other users.')
    old_user = ad.Dict(await USER_DAO.read(user_id=user_id))
    if not old_user:
        raise HTTPException(status_code=404, detail=f'Unable to find user {user_id}.')

    # Check if new email is in use.
    if user_to_patch.email:
        users = await USER_DAO.read_multi(search={'email': user_to_patch.email})
        if len(users) > 0 and users[0]['id'] != user_id:
            raise HTTPException(
                status_code=422,
                detail=f'Unable to update user {old_user.username} {user_id} to email: '
                       '{user_to_update.email} because that email is already in use.')

    user = ad.Dict(user_to_patch.dict())
    # set info that cannot be changed from user
    LOGGER.debug('Setting metadata and non changed data.')
    user.username = old_user.username
    user.metadata.date_created = old_user.metadata.date_created
    user.metadata.created_by = old_user.metadata.created_by
    user.metadata.last_modified = datetime.now(timezone.utc)
    user.metadata.modified_by = acting_username
    user.verified = old_user.verified
    user.access = old_user.access
    if not user.email:
        user.email = old_user.email
    else:
        user.verified = False  # reset because they are setting a new email that must be verified

    # hash new password
    if user_to_patch.password:
        salt, key = user_utils.hash_password(password=user_to_patch.password)
        user.salt = salt
        user.hashed_password = key
    else:
        user.salt = old_user.salt
        user.hashed_password = old_user.hashed_password
    user_to_store = UserCreateToDAO(**user)
    LOGGER.debug(f'User to store is: {user_to_store}')

    await USER_DAO.update(user_id=user_id, user=user_to_store.dict())
    return await USER_DAO.read(user_id=user_id)


@router.delete(
    "/userid/{user_id}",
    tags=['users'],
    status_code=204)
async def delete_user(
        user_id: ObjectIdStr,
        acting_username: str = Depends(get_token_header)):
    """
    Delete a user.

    A user must have admin access to delete other users.

    **user_id** - The user id of the user to delete.

    **returns** - No content.
    """
    LOGGER.debug(f'Deleting user: <{user_id}>.')

    acting_user = ad.Dict(await USER_DAO.read_by_username(username=acting_username))
    if not acting_user:
        raise HTTPException(
            status_code=500,
            detail=f'Unable to get user data for: {acting_username}. Cannot proceed with deleting '
                   f'of {user_id}.')
    LOGGER.debug(f'User access level is: {acting_user.access}. Trying to delete {user_id} as user '
                 f'{acting_user.id}.')
    if not acting_user.access == Access['admin'] and acting_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail='User does not have access to delete other users.')
    await USER_DAO.delete(user_id=user_id)
