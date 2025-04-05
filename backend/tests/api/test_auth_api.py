from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_register(temp_user):
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "testpassword", "name": "Test"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] is not None

def test_login_existing_user(db_user):
    response = client.post(
        "/auth/login", 
        data={"username": db_user["email"], "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] is not None

def test_login_not_existing_user(db_user):
    response = client.post(
        "/auth/login", 
        data={"username": db_user["email"], "password": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Invalid email or password"