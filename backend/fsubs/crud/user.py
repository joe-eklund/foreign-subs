"""CRUD functions for users."""

import logging
from typing import Any, Dict, List

from bson.objectid import ObjectId

from fsubs.models.user import UserCreateToDAO

LOGGER = logging.getLogger(__name__)


class UserDAO():
    """The DAO for interacting with users."""

    def __init__(self, client):
        """
        Initialize a ``UserDAO``.

        :param client: The MongoClient object ot use for the DAO.
        """
        self.client = client

    def create(self, user: UserCreateToDAO) -> str:
        """
        Create a user.

        :param user: The ``UserInDB`` object representing the user to create.
        :returns: The id of the newly created user.
        """
        LOGGER.debug('Creating user from DAO.')
        return self.client.foreign_subs.users.insert_one(user.dict()).inserted_id

    def read(self, user_id: str) -> Dict[str, Any]:
        """
        Read a user.

        :param user_id: The id of the user to read.
        :returns: Dict representing the user.
        """
        LOGGER.debug(f'Reading user: <{user_id}>.')
        user = self.client.foreign_subs.users.find_one({'_id': ObjectId(user_id)})
        if user:
            user['id'] = str(user.pop('_id'))
        return user

    def read_by_username(self, username: str) -> Dict[str, Any]:
        """
        Read a user by username.

        :param username: The username of the user to read.
        :returns: Dict representing the user.
        """
        LOGGER.debug(f'Reading user: <{username}>.')
        user = self.client.foreign_subs.users.find_one({'username': username})
        if user:
            user['id'] = str(user.pop('_id'))
        LOGGER.debug(f'User read is: {user}.')
        return user

    def read_by_email(self, email: str) -> Dict[str, Any]:
        """
        Read a user by email.

        :param email: The email of the user to read.
        :returns: Dict representing the user.
        """
        LOGGER.debug(f'Reading user: <{email}>.')
        user = self.client.foreign_subs.users.find_one({'email': email})
        if user:
            user['id'] = str(user.pop('_id'))
        LOGGER.debug(f'User read is: {user}.')
        return user

    def read_multi(self, limit=100, skip=0) -> List[Dict[str, Any]]:
        """
        Read multiple users.

        :param limit: The number of users to read.
        :param skip: The number of users to skip.
        :returns: A list of Dicts representing users.
        """
        LOGGER.debug(f'Reading all user with limit: <{limit}> and skip: <{skip}>.')
        users = self.client.foreign_subs.users.find().skip(skip).limit(limit)
        users = list(users)
        for user in users:
            user['id'] = str(user.pop('_id'))
        return users
