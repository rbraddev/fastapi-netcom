import json
import asyncio


def test_create_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users/",
        data=json.dumps(
            {"email": "foo@bar.com", "username": "foo_bar", "full_name": "foo bar", "password": "password123"}
        ),
    )

    assert response.status_code == 201
    assert response.json()["username"] == "foo_bar"
    assert response.json()["email"] == "foo@bar.com"
    assert response.json()["role"] == "user"


def test_create_duplicate_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users/",
        data=json.dumps(
            {"email": "foo@bar.com", "username": "foo_bar", "full_name": "foo bar", "password": "password123"}
        ),
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"
