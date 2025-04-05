import pytest
from fastapi.testclient import TestClient
from loguru import logger

from backend.app.main import app
from backend.app.dependencies.auth import get_current_user_id

client = TestClient(app)


@pytest.fixture(scope="function")
def override_dependency(db_user):
    app.dependency_overrides[get_current_user_id] = lambda: db_user["id"]
    yield
    app.dependency_overrides.clear()


def test_create_recipe(temp_recipe, db_user, override_dependency):
    response = client.post("/recipe", json=temp_recipe)
    assert response.status_code == 200
    data = response.json()
    logger.debug(data)
    assert data["name"] == temp_recipe["name"]
    assert data["instructions"] == temp_recipe["instructions"]
    assert data["user_id"] == db_user["id"]


def test_get_recipe(db_recipe, override_dependency):
    response = client.get(f"/recipe/{db_recipe['id']}")
    assert response.status_code == 200
    data = response.json()
    logger.debug(data)
    assert data["name"] == db_recipe["name"]
    assert data["instructions"] == db_recipe["instructions"]
    assert data["user_id"] == db_recipe["user_id"]


def test_update_recipe(db_recipe, temp_recipe, override_dependency):
    update_data = {
        "name": temp_recipe["name"],
        "instructions": temp_recipe["instructions"],
        "id": db_recipe["id"],
    }
    response = client.put(f"/recipe/{db_recipe['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    logger.debug(data)
    assert data["name"] == temp_recipe["name"]
    assert data["instructions"] == temp_recipe["instructions"]
    assert data["user_id"] == db_recipe["user_id"]


def test_delete_recipe(db_recipe, override_dependency):
    response = client.delete(f"/recipe/{db_recipe['id']}")
    assert response.status_code == 200
    data = response.json()
    logger.debug(data)
    assert data["id"] == db_recipe["id"]


def test_get_recipes_by_user_id(db_user, db_recipe, override_dependency):
    response = client.get("/recipes")
    assert response.status_code == 200
    data = response.json()
    logger.debug(data)
    assert len(data) == 1
    assert data[0]["name"] == db_recipe["name"]
    assert data[0]["instructions"] == db_recipe["instructions"]
    assert data[0]["user_id"] == db_user["id"]
