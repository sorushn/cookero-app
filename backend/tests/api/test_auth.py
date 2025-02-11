from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_register():
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "password", "name": "Test"})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["token"] is not None

def test_login():
    response = client.post("/auth/login", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["token"] is not None