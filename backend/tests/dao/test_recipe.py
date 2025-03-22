import pytest
from loguru import logger

from backend.app.schemas.recipe import RecipeCreate
from backend.app.dao.recipe import recipeDAO
from backend.app.core.db import driver
from backend.app.schemas.recipe import RecipeUpdate
from backend.app.dao.user import authdao
from backend.app.schemas.user import UserCreate

@pytest.fixture
def temp_recipe(db_user):
    recipe = {
        "name": "Test Recipe",
        "instructions": "Test Instructions",
        "user_id": db_user["id"]
    }
    yield recipe
    driver.execute_query("MATCH (r:Recipe {name: $name}) DETACH DELETE r", name=recipe["name"])

def test_create(temp_recipe):
    records = recipeDAO.create(RecipeCreate(**temp_recipe))
    assert records['name'] == temp_recipe["name"]
    assert records['instructions'] == temp_recipe["instructions"]

def test_update(temp_recipe):
    recipe = recipeDAO.create(RecipeCreate(**temp_recipe))
    update_payload = recipeDAO.update(RecipeUpdate(id=recipe["id"], name=temp_recipe["name"], instructions=temp_recipe["instructions"]))
    assert update_payload['name'] == temp_recipe["name"]
    assert update_payload['instructions'] == temp_recipe["instructions"]

def test_get_by_id(temp_recipe):
    recipe = recipeDAO.create(RecipeCreate(**temp_recipe))
    get_by_id_payload = recipeDAO.get_by_id(recipe["id"])
    assert get_by_id_payload['id'] == recipe["id"]

def test_delete(temp_recipe):
    recipe = recipeDAO.create(RecipeCreate(**temp_recipe))
    _ = recipeDAO.delete(recipe["id"])
    get_by_id_payload = recipeDAO.get_by_id(recipe["id"])
    assert get_by_id_payload['error'] == "Recipe not found"

@pytest.fixture
def db_user():
    user = {
        "email": "test@example.com",
        "password": "testpassword",
        "name": "Test User"
    }
    user = authdao.register(UserCreate(**user))
    yield user
    driver.execute_query("MATCH (u:User {email: $email}) DETACH DELETE u", email=user["email"])

def test_get_by_user_id(db_user):
    recipe = recipeDAO.create(RecipeCreate(name="Test Recipe", instructions="Test Instructions", user_id=db_user["id"]))
    retrieved_recipe = recipeDAO.get_by_user_id(db_user["id"])
    assert len(retrieved_recipe) == 1
    assert retrieved_recipe[0]['r']['name'] == recipe['name']
    assert retrieved_recipe[0]['r']['instructions'] == recipe['instructions']
    assert retrieved_recipe[0]['r']['id'] == recipe['id']