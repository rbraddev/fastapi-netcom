from app.core.security import create_access_token


def test_create_access_token():
    token = create_access_token(data={"sub": "foooooo"}, expiry=10, key="its_shhhhuuuper_secret", algorithm="HS256")

    assert isinstance(token, bytes)
