import json

import pytest


@pytest.mark.parametrize(
    "credentials, status_code, detail",
    [
        [
            {"username": "foo", "password": "password123"},
            401,
            "Incorrect username or password",
        ],
        [
            {"username": "foo_bar", "password": "password"},
            401,
            "Incorrect username or password",
        ],
    ]
)
def test_get_token_with_invalid_credentials(test_app_with_db, credentials, status_code, detail):
    test_app_with_db.post(
        "/users/",
        data=json.dumps(
            {"email": "foo@bar.com", "username": "foo_bar", "full_name": "foo bar", "password": "password123"}
        ),
    )

    response = test_app_with_db.post("/auth/token", auth=(credentials["username"], credentials["password"]))

    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_get_token_with_valid_credentials(test_app_with_db):
    test_app_with_db.post(
        "/users/",
        data=json.dumps(
            {"email": "foo@bar.com", "username": "foo_bar", "full_name": "foo bar", "password": "password123"}
        ),
    )

    response = test_app_with_db.post("/auth/token", auth=("foo_bar", "password123"))

    assert response.status_code == 200
    assert "access_token" in response.json().keys()
