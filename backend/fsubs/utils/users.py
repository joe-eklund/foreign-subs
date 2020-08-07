"""Utility functions for users."""
import binascii
import hashlib
import logging
import os
from typing import Tuple

from fastapi import HTTPException

from fsubs.models.user import Access

LOGGER = logging.getLogger(__name__)


def hash_password(password: str) -> Tuple[str, str]:
    """
    Salt and hash the given password.

    :param password: The password to salt and hash.
    :returns: A tuple of the salt and hashed password both encoded in ascii.
    """
    LOGGER.debug('Hashing password with password...ha you wish.')
    salt = os.urandom(32)
    salt_ascii = binascii.hexlify(salt).decode().encode('ascii')
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt_ascii,
        100000,
    )
    return salt_ascii.decode(), binascii.hexlify(key).decode()


def verify_password(password: str, salt: str, key: str) -> bool:
    """
    Verify the given password against the given salt and key.

    :param password: The password to check.
    :param salt: The salt to use. Should be encoded in ascii.
    :param key: The key to use. Should be encoded in ascii.
    :returns: True if given a valid password, False otherwise.
    """
    LOGGER.debug("Verifying password.")
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('ascii'),
        100000
    )
    return binascii.hexlify(new_key).decode() == key


async def check_access(
        user: dict,
        username: str,
        obj_to_check: dict = None,
        level: Access = Access.basic,):
    """
    Check that the given user has at least the given access level.

    :param user: The user object to check.
    :param username: The username of the user. Useful for error message if the user read resulted
    in `None`.
    :param obj_to_check: If supplied, and the given user matches the creator of the object, then
    allow access even if the user doesn't have the required level.
    :param level: The access level required.
    :raises HTTPException: If no user was supplied or if the user doesn't have the required access.
    """
    LOGGER.info(f'Checking {username} has at least {level} access.')
    if not user:
        raise HTTPException(
            status_code=500,
            detail=f'Unable to get user data for: {username}. Cannot proceed with action.')
    if obj_to_check and obj_to_check.get('metadata', {}).get('created_by') == username:
        return
    if not user.access >= level:
        raise HTTPException(
            status_code=403,
            detail=f'User {username} does not have at least level {level.name} to perform action.')
