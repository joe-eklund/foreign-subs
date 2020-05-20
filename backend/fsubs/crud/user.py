"""CRUD functions for users."""

import logging

from fsubs.models.user import UserInDB

LOGGER = logging.getLogger(__name__)


class UserDAO():
    """The DAO for interacting with users."""

    def __init__(self, client):
        """
        Initialize a ``UserDAO``.

        :param client: The MongoClient object ot use for the DAO.
        """
        self.client = client

    def create(self, user: UserInDB) -> str:
        """
        Create a user.

        :param user: The ``UserInDB`` object representing the user to create.
        :returns: The id of the newly created user.
        """
        LOGGER.debug('Creating user from DAO.')
        return self.client.foreign_subs.users.insert_one(user).inserted_id
