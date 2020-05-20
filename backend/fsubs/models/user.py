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

    **email** - What email to use for the user.
    **username** - What username to use for the user.
    **access** - What access level the user is to have.
    """

    email: str
    username: str
    access: Access = Access['basic']


class UserCreate(UserBase):
    """
    User creation data.

    **password** - What password to use for the user.
    """

    password: str


class UserInDB(UserBase):
    """
    The User stored in the db.

    **id** - The id of the user stored in the database.

    **hashed_password** - The hashed version of the user's password.
    """

    id: str
    hashed_password: str
    metadata: Metadata = Metadata()
