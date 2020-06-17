"""Utility functions for users."""
import binascii
import hashlib
import logging
import os
from typing import Tuple

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
    new_key = binascii.hexlify(new_key).decode()
    LOGGER.debug(f'New key is: {new_key}.')
    return new_key == key
