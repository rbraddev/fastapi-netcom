from datetime import datetime, timedelta

import jwt
from jwt import PyJWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.config import get_settings, Settings
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
    user = await User.filter(email=username).first()
    if not user or (password and not user.verify_password(password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), settings: Settings = Depends(get_settings)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.auth_secret_key, algorithms=[settings.token_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = await authenticate_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
