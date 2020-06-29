import os
from typing import Generator, List

import pytest
from starlette.testclient import TestClient
from tortoise import run_async
from tortoise.contrib.test import finalizer, initializer

from app.config import Settings, get_settings
from app.core.security.utils import create_access_token
from app.main import create_application
from app.models.tortoise.users import User

AUTH_SECRET_KEY = "testingkey123"


def get_settings_override():
    return Settings(
        testing=1,
        database_url=os.environ.get("DATABASE_TEST_URL"),
        auth_secret_key=AUTH_SECRET_KEY,
        token_algorithm="HS256",
    )


@pytest.fixture(scope="session")
def test_app() -> Generator:
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def test_app_with_db() -> Generator:
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    initializer(db_url=os.environ.get("DATABASE_TEST_URL"), modules=["app.models.tortoise.users"])
    run_async(add_users())

    with TestClient(app) as test_client:
        yield test_client

    finalizer()


@pytest.fixture(scope="module")
def event_loop(test_app_with_db: TestClient) -> Generator:
    yield test_app_with_db.task.get_loop()


@pytest.fixture
def get_access_token(test_app_with_db) -> str:
    def _create_access_token(username: str, expiry: int = 15, scopes: List[str] = []):
        return create_access_token(
            data={"sub": username, "scopes": scopes}, expiry=expiry, key=AUTH_SECRET_KEY, algorithm="HS256"
        ).decode("utf-8")

    return _create_access_token


async def add_users() -> None:
    user_list = [
        {"username": "user", "email": "user@test.com", "full_name": "user user", "password": "pass123"},
        {
            "username": "tech",
            "email": "tech@test.com",
            "full_name": "tech user",
            "password": "pass123",
            "role": "tech",
            "scopes": "tech:run"
        },
        {
            "username": "admin",
            "email": "admin@test.com",
            "full_name": "admin_user",
            "password": "pass123",
            "role": "admin",
            "scopes": "admin"
        },
    ]
    for user in user_list:
        u = User(**user)
        u.set_password(user.get("password"))
        await u.save()
