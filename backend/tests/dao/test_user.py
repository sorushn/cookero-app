import pytest
from loguru import logger

from backend.app.schemas.user import UserCreate
from backend.app.dao.user import AuthDAO
from backend.app.settings import settings
from backend.app.core.db import driver

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
    dao = AuthDAO()
    records = dao.register(UserCreate(email=temp_user["email"], password=temp_user["password"], name=temp_user["name"]))
    assert records['email'] == temp_user["email"]
    assert records['name'] == temp_user["name"]

def test_register_duplicate_email(temp_user):
    dao = AuthDAO()
    _ = dao.register(UserCreate(email=temp_user["email"], password=temp_user["password"], name=temp_user["name"]))
    records = dao.register(UserCreate(email=temp_user["email"], password=temp_user["password"], name=temp_user["name"]))
    assert records["error"] == "User with this email already exists"

def test_authenticate(temp_user):
    dao = AuthDAO()
    _ = dao.register(UserCreate(email=temp_user["email"], password=temp_user["password"], name=temp_user["name"]))
    authenticate_payload = dao.authenticate(temp_user["email"], temp_user["password"])
    assert "token" in authenticate_payload
    assert authenticate_payload["token"] is not None
