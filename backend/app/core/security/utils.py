from datetime import datetime, timedelta

import jwt
from jwt import PyJWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.config import get_settings, Settings
from app.core.security.errors import credential_error
from app.models.tortoise.users import User
from app.models.pydantic.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(data: dict, expiry: int, key: str, algorithm: str) -> bytes:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expiry)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)
    return encoded_jwt


async def authenticate_user(username: str, password: str = None) -> User:
    if None in [username, password]:
        raise credential_error("Incorrect username or password", "Basic")
    user = await User.filter(username=username).first()
    if not user or not user.verify_password(password):
        raise credential_error("Incorrect username or password", "Basic")
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), settings: Settings = Depends(get_settings)) -> User:
    try:
        payload = jwt.decode(token, settings.auth_secret_key, algorithms=[settings.token_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credential_error("Could not validate token", "Bearer")
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credential_error("Could not validate token", "Bearer")
    user = await User.filter(username=token_data.username).first()
    if user is None:
        raise credential_error("Could not validate token", "Bearer")
    return user
