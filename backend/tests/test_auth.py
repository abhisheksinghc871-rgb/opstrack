def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={"email": "bob@opstrack.dev", "full_name": "Bob Builder", "password": "supersecret1"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["user"]["email"] == "bob@opstrack.dev"
    assert "access_token" in body


def test_register_duplicate_email_rejected(client):
    payload = {"email": "dup@opstrack.dev", "full_name": "Dup User", "password": "supersecret1"}
    first = client.post("/api/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/api/auth/register", json=payload)
    assert second.status_code == 409


def test_login_success(client):
    client.post(
        "/api/auth/register",
        json={"email": "carol@opstrack.dev", "full_name": "Carol Chen", "password": "supersecret1"},
    )
    response = client.post(
        "/api/auth/login", json={"email": "carol@opstrack.dev", "password": "supersecret1"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password(client):
    client.post(
        "/api/auth/register",
        json={"email": "dave@opstrack.dev", "full_name": "Dave Park", "password": "supersecret1"},
    )
    response = client.post(
        "/api/auth/login", json={"email": "dave@opstrack.dev", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_me_requires_token(client):
    response = client.get("/api/users")
    assert response.status_code == 401


def test_me_returns_current_user(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "alice@opstrack.dev"
