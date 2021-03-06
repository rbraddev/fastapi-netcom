import logging

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import get_settings, Settings
from app.core.security.utils import create_access_token, authenticate_user
from app.models.pydantic.auth import Token

router = APIRouter()
httpbasic = HTTPBasic()

log = logging.getLogger(__name__)


@router.post("/token", response_model=Token)
async def get_access_token(
    credentials: HTTPBasicCredentials = Depends(httpbasic), settings: Settings = Depends(get_settings),
):
    expiry, key, algorithm = (
        settings.auth_token_expiry,
        settings.auth_secret_key,
        settings.token_algorithm,
    )
    user = await authenticate_user(credentials.username, credentials.password)
    log.info(f"user scopes: {user.scopes}")
    access_token = create_access_token(
        data={"sub": user.username, "scopes": [scope for scope in user.scopes.split(",")]},
        expiry=expiry,
        key=key,
        algorithm=algorithm,
    )
    return {"access_token": access_token, "token_type": "bearer"}
