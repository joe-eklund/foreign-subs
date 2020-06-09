"""Defines logic used for endpoints at ``/authenticate``."""

import logging
from datetime import timedelta

import addict as ad
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED

from fsubs.config.config import Config
from fsubs.utils import auth as auth_utils

router = APIRouter()

LOGGER = logging.getLogger(__name__)
CONFIG = Config()
base_url = CONFIG["app"]["base_url"]
token_url = f'{base_url or ""}/authenticate'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)


async def get_token_header(token: str = Depends(oauth2_scheme)) -> str:
    """Get the token from the header of the request."""
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            CONFIG["app"]["jwt_secret"],
            algorithms=[CONFIG["app"]["jwt_algorithm"]])
        username: str = payload.get("identity")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    return username


@router.post("", tags=["authenticate"], status_code=201)
async def authenticate(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate the user.

    **username**: The username to authenticate with.
    **password**: The password to authenticate with.
    """
    username = form_data.username
    password = form_data.password
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # TODO auth user against db
    authenticated = True

    if authenticated is False:
        raise credentials_exception
    elif authenticated is None:
        msg = 'Unexpected authentication error.'
        LOGGER.error(msg)
        raise HTTPException(500, detail=msg)

    # Generate an access token
    access_token_expires = timedelta(hours=int(CONFIG['app']['jwt_expires_hours']))
    token = auth_utils.create_access_token(
        data={"identity": username},
        expires_delta=access_token_expires)
    LOGGER.debug(f'Generated access token for {username}: {token}')
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "",
    tags=["authenticate"],
    response_model=str,
    dependencies=[Depends(get_token_header)],
    status_code=200
)
async def check_token():
    """Check the authentication token."""
    return 'You have a valid token.'
