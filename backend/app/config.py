import logging
import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    server_host: str = os.getenv("SERVER_HOST", "localhost:8000")
    database_url: AnyUrl = os.environ.get("DATABASE_URL")
    auth_secret_key: str = os.environ.get("AUTH_SECRET_KEY", os.urandom(32).hex())
    auth_token_expiry: int = os.environ.get("AUTH_TOKEN_EXPIRY", 10)
    new_user_token_expiry: int = os.environ.get("NEW_USER_TOKEN_EXPIRY", 10)
    password_reset_token_expiry: int = os.environ.get("PASSWORD_RESET_TOKEN_EXPIRY", 10)
    token_algorithm: str = os.environ.get("TOKEN_ALGORITHM", "HS256")
    send_emails: bool = os.environ.get("SEND_EMAILS", True)
    smtp_host: str = os.environ.get("SMTP_HOST")
    smtp_port: int = os.environ.get("SMTP_PORT")
    smtp_tls: bool = os.environ.get("SMTP_TLS")
    smtp_user: str = os.environ.get("SMTP_USER")
    smtp_password: str = os.environ.get("SMTP_PASSWORD")
    emails_from_name: str = os.environ.get("EMAILS_FROM_NAME")
    emails_from_email: str = os.environ.get("EMAILS_FROM_EMAIL")


@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
