import pytest
from fastapi import HTTPException
from fastapi.security import SecurityScopes

from app.core.security.utils import create_access_token, authenticate_user, get_current_user
from app.models.tortoise.users import User
from tests.conftest import get_settings_override


def test_create_access_token():
    token = create_access_token(data={"sub": "user"}, expiry=10, key="its_shhhhuuuper_secret", algorithm="HS256")

    assert isinstance(token, bytes)


@pytest.mark.asyncio
async def test_authenticate_user_valid_with_pass():
    user = await authenticate_user("user", "pass123")

    assert isinstance(user, User)
    assert user.username == "user"


@pytest.mark.asyncio
async def test_authenticate_user_valid_without_pass():
    with pytest.raises(HTTPException):
        await authenticate_user("user")


@pytest.mark.asyncio
async def test_authenticate_user_invalid():
    with pytest.raises(HTTPException):
        await authenticate_user("user", "letmein")


@pytest.mark.asyncio
async def test_get_current_user_valid(get_access_token):
    access_token = get_access_token("user", scopes=["user:test"])

    class MockScopes:
        scopes = ["user:test"]

        def scope_str(self):
            return str(self.scopes)

    user = await get_current_user(MockScopes, access_token, get_settings_override())

    assert isinstance(user, User)


@pytest.mark.parametrize("user", ["", "nouser"])
@pytest.mark.asyncio
async def test_get_current_user_invalid_user(get_access_token, user):
    access_token = get_access_token(user)
    with pytest.raises(HTTPException):
        await get_current_user(access_token, get_settings_override())


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    access_token = "this_is_not_a_valid_token"
    with pytest.raises(HTTPException):
        await get_current_user(access_token, get_settings_override())
