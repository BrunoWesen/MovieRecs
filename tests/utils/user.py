from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_user(username: str, json: dict=None) -> str:
    body: dict = {"username": username, "watched_movies": []} if json is None else json
    return client.post("/usuarios", json=body).json()['_id']
