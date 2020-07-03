import logging
import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    database_url: AnyUrl = os.environ.get("DATABASE_URL")
    auth_secret_key: str = os.environ.get("AUTH_SECRET_KEY", os.urandom(32).hex())
    auth_token_expiry: int = os.environ.get("AUTH_TOKEN_EXPIRY", 10)
    token_algorithm: str = os.environ.get("TOKEN_ALGORITHM", "HS256")


@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
