import os

import pytest
from starlette.testclient import TestClient
# from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.test import initializer, finalizer

from app.config import Settings, get_settings
from app.main import create_application


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


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
    initializer(
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules=["app.models.tortoise.users"]
    )
    # register_tortoise(
    #     app,
    #     db_url=os.environ.get("DATABASE_TEST_URL"),
    #     modules={"models": ["app.models.tortoise.users"]},
    #     generate_schemas=True,
    #     add_exception_handlers=True,
    # )
    with TestClient(app) as test_client:
        yield test_client

    finalizer()
    # run_async(remove_db())


# async def remove_db():
#     conn = Tortoise.get_connection()
#     database = os.environ.get("DATABASE_TEST_URL").split("/")[-1]
#     await conn.execute_query(f"drop database {database};")
#     await conn.close()
