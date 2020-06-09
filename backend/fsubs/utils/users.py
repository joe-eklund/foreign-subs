"""Utility functions for users."""
import hashlib
import logging
import os
from typing import Tuple

LOGGER = logging.getLogger(__name__)


def hash_password(password: str) -> Tuple[str, str]:
    """
    Salt and hash the given password.

    :param password: The password to salt and hash.
    :returns: A tuple of the salt and hashed password.
    """
    LOGGER.debug('Hashing password with password...ha you wish.')
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000,
    )
    return salt, key


def verify_password(password: str, salt: str, key: str) -> bool:
    """
    Verify the given password against the given salt and key.

    :param password: The password to check.
    :param salt: The salt to use.
    :param key: The key to use.
    :returns: True if given a valid password, False otherwise.
    """
    LOGGER.debug("Verifying password.")
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt, 
        100000
    )
    return new_key == key
