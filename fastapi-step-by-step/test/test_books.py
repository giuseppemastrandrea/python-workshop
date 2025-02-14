from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# 🔹 Test creazione libro
def test_create_book():
    response = client.post(
        "/api/books/", json={"title": "Dune", "published_date": "1965-06-01"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Dune"
