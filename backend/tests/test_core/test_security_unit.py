import pytest

from app.core.security import create_access_token


def test_create_access_token():
    token = create_access_token(data={"sub": "foooooo"}, expiry=10, key="its_shhhhuuuper_secret", algorithm="HS256")

    assert isinstance(token, bytes)


@pytest.mark.asyncio
async def test_authenticate_user():
    pass
