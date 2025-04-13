from fastapi.testclient import TestClient

from app.main import app
from tests.utils.user import create_user

client = TestClient(app)


def test_list_movies():
    response = client.get("/filmes?limit=100")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 100


def test_recomendation_top_ratings_movies():
    username: str = "testUser"
    id: str = create_user(username)
    response = client.get(f"/filmes/{id}/recomendacoes?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

def test_recomendation_gender_movies():
    username: str = "testUser"
    body: dict = {"username": username, "watched_movies": [{"tconst": "tt0126029", "rating": 2.5}]}
    id: str = create_user(username, body)
    response = client.get(f"/filmes/{id}/recomendacoes?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    contain_gender: bool = True
    for movie in data:
        if not contain_gender:
            break
        contain_gender = 'Adventure' in movie['genres']
    assert contain_gender


def test_recomendation_film_crew_movies():
    username: str = "testUser"
    body: dict = {"username": username, "watched_movies": [{"tconst": "tt0126029", "rating": 2.5}]}
    id: str = create_user(username, body)
    gender_recomendation: dict = client.get(f"/filmes/{id}/recomendacoes?limit=1").json()[0]
    client.put(f"/usuarios/{id}/assistidos", json={"tconst": "tt0126029", "rating": 10.0})
    response = client.get(f"/filmes/{id}/recomendacoes?limit=1")
    assert response.status_code == 200
    data = response.json()
    assert data[0] != gender_recomendation


def test_recomendation_user_not_exist():
    response = client.get("/filmes/Skeepan/recomendacoes?limit=5")
    assert response.status_code == 404
