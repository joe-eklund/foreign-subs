"""User models."""
from enum import Enum
import re

from pydantic import BaseModel, validator
from pymongo import MongoClient

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


class UserCreate(BaseModel):
    """
    User creation data.

    **password** - What password to use for the user.
    """

    email: str
    username: str
    password: str

    @validator('email')
    def check_email(cls, v):
        """Ensure email is valid."""
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$' 
        if not v:
            raise ValueError('Cannot have empty string for email.')
        if not re.search(regex, v):
            raise ValueError('Invalid email.')
        return v

    @validator('username')
    def check_username(cls, v):
        """Ensure username is valid."""
        if not v:
            raise ValueError('Cannot have empty string for username.')
        return v

    @validator('password')
    def check_password(cls, v):
        """Ensure password is valid."""
        if not v:
            raise ValueError('Cannot have empty string for password.')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        if len(v) > 1024:
            raise ValueError('Password cannot be longer than 1024 characters.')
        return v


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
