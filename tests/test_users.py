from fastapi.testclient import TestClient

from app.main import app
from tests.utils.user import create_user

client = TestClient(app)


def test_create_user():
    username: str = "testUser"
    response = client.post("/usuarios", json={"username": username, "watched_movies": []})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username


def test_list_users():
    response = client.get("/usuarios")
    assert response.status_code == 200


def test_get_user():
    username: str = "testUser"
    id: str = create_user(username)
    response = client.get(f"/usuarios/{id}")
    assert response.status_code == 200
    data = response.json()
    assert data['_id'] == id
    assert data['username'] == username

def test_get_user_not_exist():
    response = client.get("/usuarios/Prostagma")
    assert response.status_code == 404

def test_insert_watched_movie_users():
    username: str = "testUser"
    id: str = create_user(username)
    response = client.put(f"/usuarios/{id}/assistidos", json={"tconst": "tt0126029"})
    assert response.status_code == 200
    data = response.json()
    assert len(data['watched_movies']) == 1


def test_update_watched_movie_users():
    username: str = "testUser"
    body: dict = {"username": username, "watched_movies": [{"tconst": "tt0126029", "rating": 2.5}]}
    id: str = create_user(username, body)
    response = client.put(f"/usuarios/{id}/assistidos", json={"tconst": "tt0126029", "rating": 10.0})
    assert response.status_code == 200
    data = response.json()
    assert data['watched_movies'][0] == {"tconst": "tt0126029", "rating": 10.0}
