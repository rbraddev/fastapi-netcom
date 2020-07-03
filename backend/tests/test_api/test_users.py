import pytest


def test_create_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users/",
        json={"email": "new_user@test.com", "username": "new_user", "full_name": "new user", "password": "pass123"},
    )

    assert response.status_code == 201
    assert response.json()["username"] == "new_user"


def test_create_duplicate_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users/", json={"email": "user@test.com", "username": "user", "full_name": "user user", "password": "pass123"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username/email already exists"


def test_create_user_with_incomplete_payload(test_app_with_db):
    response = test_app_with_db.post("/users/", json={"username": "invalidtest"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {"loc": ["body", "email"], "msg": "field required", "type": "value_error.missing"},
            {"loc": ["body", "full_name"], "msg": "field required", "type": "value_error.missing"},
            {"loc": ["body", "password"], "msg": "field required", "type": "value_error.missing"},
        ]
    }


@pytest.mark.parametrize("user, scopes", [["user", ["user:read"]], ["tech", ["tech:run"]]])
def test_get_all_users_unauthorised(test_app_with_db, get_access_token, user, scopes):
    access_token = get_access_token(username=user, scopes=scopes)
    response = test_app_with_db.get("/users/", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 401


def test_get_all_users_authorised(test_app_with_db, get_access_token):
    access_token = get_access_token(username="admin", scopes=["admin"])
    response = test_app_with_db.get("/users/", headers={"Authorization": f"Bearer {access_token}"})
    response_list = response.json()

    assert response.status_code == 200
    assert len(list(filter(lambda user: user["username"] == "user", response_list))) == 1


def test_get_me(test_app_with_db, get_access_token):
    access_token = get_access_token("user")
    response = test_app_with_db.get("/users/me/", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json()["username"] == "user"


def test_get_me_expired_token(test_app_with_db, get_access_token):
    access_token = get_access_token("user", -1)
    response = test_app_with_db.get("/users/me/", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate token"


def test_get(test_app_with_db, get_access_token):
    username = "user"
    access_token = get_access_token(username)

    response = test_app_with_db.get(f"/users/{username}/", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json()["username"] == username


def test_get_invalid_user(test_app_with_db, get_access_token):
    username = "nouser"
    access_token = get_access_token(username)

    response = test_app_with_db.get(f"/users/{username}/", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate token"
