from backend.app.dao.user import AuthDAO
from backend.app.settings import settings
from backend.app.core.db import driver
import pytest

@pytest.fixture
def temp_user():
    user = {
        "email": "test@example.com",
        "name": "Test",
        "password": "password"
    }
    yield user
    driver.execute_query("MATCH (u:User {email: $email}) DETACH DELETE u", email=user["email"])

def test_register(temp_user):
    dao = AuthDAO(jwt_secret=settings.get("security", "SECRET_KEY"))
    payload = dao.register(email=temp_user["email"], plain_password=temp_user["password"], name=temp_user["name"])
    assert payload["email"] == temp_user["email"]
    assert payload["name"] == temp_user["name"]

def test_authenticate(temp_user):
    dao = AuthDAO(jwt_secret=settings.get("security", "SECRET_KEY"))
    _ = dao.register(email=temp_user["email"], plain_password=temp_user["password"], name=temp_user["name"])
    authenticate_payload = dao.authenticate(email=temp_user["email"], plain_password=temp_user["password"])
    assert "token" in authenticate_payload
    assert authenticate_payload["token"] is not None
