import asyncio

import pytest
from fastapi import HTTPException

from app.core.security.utils import create_access_token, authenticate_user, get_current_user
from app.models.tortoise.users import User
from tests.conftest import get_settings_override


def test_create_access_token():
    token = create_access_token(data={"sub": "user"}, expiry=10, key="its_shhhhuuuper_secret", algorithm="HS256")

    assert isinstance(token, bytes)


def test_authenticate_user_valid_with_pass(event_loop: asyncio.AbstractEventLoop):
    user = event_loop.run_until_complete(authenticate_user("user", "pass123"))

    assert isinstance(user, User)
    assert user.username == "user"


def test_authenticate_user_valid_without_pass(event_loop: asyncio.AbstractEventLoop):
    with pytest.raises(HTTPException):
         event_loop.run_until_complete(authenticate_user("user"))


def test_authenticate_user_invalid(event_loop: asyncio.AbstractEventLoop):
    with pytest.raises(HTTPException):
        event_loop.run_until_complete(authenticate_user("user", "letmein"))


def test_get_current_user_valid(event_loop_no_oauth2: asyncio.AbstractEventLoop, get_access_token):
    access_token = get_access_token("user")
    user = event_loop_no_oauth2.run_until_complete(get_current_user(access_token, get_settings_override()))

    assert isinstance(user, User)


@pytest.mark.parametrize("user", ["", "nouser"])
def test_get_current_user_invalid_user(event_loop_no_oauth2: asyncio.AbstractEventLoop, get_access_token, user):
    access_token = get_access_token(user)
    with pytest.raises(HTTPException):
        user = event_loop_no_oauth2.run_until_complete(get_current_user(access_token, get_settings_override()))


def test_get_current_user_invalid_token(event_loop_no_oauth2: asyncio.AbstractEventLoop):
    access_token = "this_is_not_a_valid_token"
    with pytest.raises(HTTPException):
        event_loop_no_oauth2.run_until_complete(get_current_user(access_token, get_settings_override()))
