"""User models."""
from enum import Enum
import re

from pydantic import BaseModel, validator

from fsubs.models.misc import Metadata


class OrderedEnum(Enum):
    """An ordered enum."""

    def __ge__(self, other):
        """Greater than or equal."""
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        """Greater than."""
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        """Less than or equal."""
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        """Less than."""
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Access(str, OrderedEnum):
    """The level of access for the user."""

    admin = 3
    power = 2
    basic = 1


class UserBase(BaseModel):
    """
    User base data.

    **access** - What access level the user is to have.

    **email** - What email to use for the user.

    **username** - What username to use for the user.

    **verified** - Whether or not the user has been verified.
    """

    access: Access = Access['basic']
    email: str
    username: str
    verified: bool = False
    metadata: Metadata = Metadata()


class UserUpdate(BaseModel):
    """
    User update data.

    ***email** - What email to use for the user.

    **password** - What password to use for the user.
    """

    email: str
    password: str

    @validator('email')
    def check_email(cls, v):
        """Ensure email is valid."""
        regex = '^[a-z0-9]+([\\._]?[a-z0-9]+|)[@]\\w+[.]\\w+$'
        if not v:
            raise ValueError('Cannot have empty string for email.')
        if not re.search(regex, v):
            raise ValueError('Invalid email.')
        return v

    @validator('password')
    def check_password(cls, v):
        """Ensure password is valid."""
        if not v:
            raise ValueError('Cannot have empty string for password.')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        if len(v) > 255:
            raise ValueError('Password cannot be longer than 255 characters.')
        return v


class UserCreate(UserUpdate):
    """
    User creation data.

    **username** - What username to use for the user.
    """

    username: str

    @validator('username')
    def check_username(cls, v):
        """Ensure username is valid."""
        if not v:
            raise ValueError('Cannot have empty string for username.')
        if not v.isalnum():
            raise ValueError('Username can only have alphanumeric characters.')
        return v


class UserPatch(UserUpdate):
    """User patch data."""

    email: str = None
    password: str = None


class UserRead(UserBase):
    """
    The information to return to someone reading a user.

    **id** - THe id of the user stored in the database.
    """

    id: str


class UserCreateToDAO(UserBase):
    """
    User creation data sent to DAO.

    **salt** The salt used for the user's password.

    **hashed_password** The hash of the user's password.

    **metadata** The metadata of the user.

    """

    salt: str
    hashed_password: str


class UserInDB(UserCreateToDAO):
    """
    The User stored in the db.

    **id** - The id of the user stored in the database.
    """

    id: str
