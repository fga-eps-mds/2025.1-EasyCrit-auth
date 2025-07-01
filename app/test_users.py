from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users",
        json={
            "username": "testuser",
            "email": "testemail",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "username": "testuser",
        "id": 1,
        "email": "testemail",
        "password": "testpassword",
    }

def get_access_token():
    response = client.post('/auth/login', json={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    return response.json()['access_token']


def test_get_users():
    token = get_access_token()
    response = client.get(
        "/users",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )
    assert response.status_code == 200

def test_get_user_id():
    token = get_access_token()
    response = client.get(
        "/users/1",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )
    assert response.status_code == 200

def test_update_user():
    token = get_access_token()
    response = client.put(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "testuser",
            "email": "testemail",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200

def partial_update_user():
    token = get_access_token()
    response = client.patch(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "testuser",
            "email": "testemail",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200