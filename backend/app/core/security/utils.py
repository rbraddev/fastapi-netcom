from datetime import datetime, timedelta
import logging

import jwt
from jwt import PyJWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import ValidationError

from app.config import get_settings, Settings
from app.core.security.errors import unauth_error
from app.models.tortoise.users import User
from app.models.pydantic.auth import TokenData

log = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        "me": "Read information about the current user.",
        "user:read": "Read access on user level resources",
        "user:write": "Write access on user level resources",
        "user:run": "Run access on user level resources",
        "tech:read": "Read access on tech level resources",
        "tech:write": "Write access on tech level resources",
        "tech:run": "Run access on tech level resources",
        "admin": "Superuser",
    },
)


def create_access_token(data: dict, expiry: int, key: str, algorithm: str) -> bytes:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expiry)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)
    return encoded_jwt


async def authenticate_user(username: str, password: str = None) -> User:
    if None in [username, password]:
        raise unauth_error("Incorrect username or password", "Basic")
    user = await User.filter(username=username).first()
    if not user or not user.verify_password(password):
        raise unauth_error("Incorrect username or password", "Basic")
    return user


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), settings: Settings = Depends(get_settings)
) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    try:
        payload = jwt.decode(token, settings.auth_secret_key, algorithms=[settings.token_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise unauth_error("Could not validate token", authenticate_value)
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (PyJWTError, ValidationError):
        raise unauth_error("Could not validate token", authenticate_value)
    user = await User.filter(username=token_data.username).first()
    if user is None:
        raise unauth_error("Could not validate token", authenticate_value)
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise unauth_error("Not enough permissions", authenticate_value)
    return user
