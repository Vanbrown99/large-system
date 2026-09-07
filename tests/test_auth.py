from fastapi.testclient import TestClient

from auth_service.main import app, store

client = TestClient(app)


def setup_function() -> None:
    store._users_by_email.clear()
    store._next_id = 1


def test_register_hashes_password_and_login_returns_jwt() -> None:
    response = client.post(
        "/register",
        json={"name": "Ada Admin", "email": "ada@example.com", "password": "correct horse", "role": "admin"},
    )
    assert response.status_code == 201
    assert response.json()["role"] == "admin"
    assert store.get_by_email("ada@example.com").password_hash != "correct horse"

    login = client.post("/login", json={"email": "ada@example.com", "password": "correct horse"})
    assert login.status_code == 200
    assert login.json()["access_token"]


def test_admin_route_rejects_student() -> None:
    client.post(
        "/register",
        json={"name": "Sam Student", "email": "sam@example.com", "password": "correct horse", "role": "student"},
    )
    token = client.post("/login", json={"email": "sam@example.com", "password": "correct horse"}).json()["access_token"]
    response = client.get("/admin/overview", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_invalid_login_is_rejected() -> None:
    client.post(
        "/register",
        json={"name": "Sam Student", "email": "sam@example.com", "password": "correct horse", "role": "student"},
    )
    response = client.post("/login", json={"email": "sam@example.com", "password": "wrong password"})
    assert response.status_code == 401
