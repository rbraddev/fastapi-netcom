import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer
from tortoise import run_async

from app.config import Settings, get_settings
from app.core.security import create_access_token
from app.models.tortoise.users import User
from app.main import create_application

AUTH_SECRET_KEY = "testingkey123"


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"), auth_secret_key=AUTH_SECRET_KEY)


@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def test_app_with_db():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    initializer(db_url=os.environ.get("DATABASE_TEST_URL"), modules=["app.models.tortoise.users"])
    run_async(add_users())

    with TestClient(app) as test_client:
        yield test_client

    finalizer()


@pytest.fixture
def get_access_token(test_app_with_db):
    def _create_access_token(username: str):
        return create_access_token(data={"sub": username}, expiry=15, key=AUTH_SECRET_KEY, algorithm="HS256").decode(
            "utf-8"
        )

    return _create_access_token


async def add_users():
    user_list = [
        {"username": "user", "email": "user@test.com", "full_name": "user user", "password": "pass123"},
        {
            "username": "tech",
            "email": "tech@test.com",
            "full_name": "tech user",
            "password": "pass123",
            "role": "tech",
            "access_level": 2,
        },
        {
            "username": "admin",
            "email": "admin@test.com",
            "full_name": "admin_user",
            "password": "pass123",
            "role": "admin",
            "access_level": 3,
        },
    ]
    for user in user_list:
        u = User(**user)
        u.set_password(user.get("password"))
        await u.save()
