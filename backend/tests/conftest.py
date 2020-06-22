import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.config import Settings, get_settings
from app.core.security import create_access_token
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


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    initializer(db_url=os.environ.get("DATABASE_TEST_URL"), modules=["app.models.tortoise.users"])

    with TestClient(app) as test_client:
        yield test_client

    finalizer()


@pytest.fixture(scope="module")
def access_token(test_app_with_db):
    return create_access_token(data={"sub": "foo_bar"}, expiry=15, key=AUTH_SECRET_KEY, algorithm="HS256").decode(
        "utf-8"
    )
