"""Utility functions for authentication."""

import logging

import jwt
from datetime import datetime, timedelta

from fsubs.config.config import Config

LOGGER = logging.getLogger(__name__)
CONFIG = Config()


def create_access_token(*, data: dict, expires_delta: timedelta = None) -> bytes:
    """Create an access token for bearer authentication."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, CONFIG['app']['jwt_secret'],
                             algorithm=CONFIG['app']['jwt_algorithm'])
    return encoded_jwt
