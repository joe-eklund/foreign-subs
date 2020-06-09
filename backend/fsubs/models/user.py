"""User models."""
from enum import Enum

from pydantic import BaseModel

from fsubs.models.misc import Metadata


class Access(str, Enum):
    """The level of access for the user."""

    admin = 'admin'
    power = 'power'
    basic = 'basic'


class UserBase(BaseModel):
    """
    User base data.

    **access** - What access level the user is to have.
    **email** - What email to use for the user.
    **username** - What username to use for the user.

    """

    access: Access = Access['basic']
    email: str
    username: str
    verified: bool = False


class UserCreate(UserBase):
    """
    User creation data.

    **password** - What password to use for the user.
    """

    password: str


class UserCreateToDAO(UserBase):
    """
    User creation data sent to DAO.

    **salt** The salt used for the user's password.

    **hashed_password** The hash of the user's password.

    **metadata** The metadata of the user.

    """

    salt: str
    hashed_password: str
    metadata: Metadata = Metadata()


class UserInDB(UserCreateToDAO):
    """
    The User stored in the db.

    **id** - The id of the user stored in the database.
    """

    id: str
