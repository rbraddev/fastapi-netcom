def test_create_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users/",
        json={"email": "foo@bar.com", "username": "foo_bar", "full_name": "foo bar", "password": "password123"},
    )

    assert response.status_code == 201
    assert response.json()["username"] == "foo_bar"
    assert response.json()["email"] == "foo@bar.com"
    assert response.json()["role"] == "user"


def test_create_duplicate_user(test_app_with_db):
    test_app_with_db.post(
        "/users/",
        json={
            "email": "duplicatefoo@bar.com",
            "username": "dup_foo_bar",
            "full_name": "foo bar",
            "password": "password123",
        },
    )
    response = test_app_with_db.post(
        "/users/",
        json={
            "email": "duplicatefoo@bar.com",
            "username": "dup_foo_bar",
            "full_name": "foo bar",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


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


def test_get_all_users(test_app_with_db, get_access_token):
    response = test_app_with_db.post(
        "/users/",
        json={"email": "foo@bar.com", "username": "get_all", "full_name": "foo bar", "password": "password123"},
    )
    username = response.json()["username"]
    access_token = get_access_token(username)
    response = test_app_with_db.get("/users/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda user: user["username"] == username, response_list))) == 1


def test_get_me(test_app_with_db, get_access_token):
    response = test_app_with_db.post(
        "/users/",
        json={"email": "foo@bar.com", "username": "get_me", "full_name": "foo bar", "password": "password123"},
    )
    username = response.json()["username"]
    access_token = get_access_token(username)

    response = test_app_with_db.get("/users/me/", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json()["username"] == username


def test_get(test_app_with_db, get_access_token):
    response = test_app_with_db.post(
        "/users/",
        json={"email": "foo@bar.com", "username": "get_username", "full_name": "foo bar", "password": "password123"},
    )
    username = response.json()["username"]
    access_token = get_access_token(username)

    response = test_app_with_db.get(f"/users/{username}/", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json()["username"] == username
