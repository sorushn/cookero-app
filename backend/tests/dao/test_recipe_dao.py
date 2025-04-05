import pytest
from loguru import logger

from backend.app.schemas.recipe import RecipeCreate
from backend.app.dao.recipe import recipeDAO
from backend.app.schemas.recipe import RecipeUpdate


def test_create(temp_recipe):
    records = recipeDAO.create(RecipeCreate(**temp_recipe))
    assert records['name'] == temp_recipe["name"]
    assert records['instructions'] == temp_recipe["instructions"]

def test_update(db_recipe, temp_recipe):
    update_payload = recipeDAO.update(RecipeUpdate(id=db_recipe["id"], name=temp_recipe["name"], instructions=temp_recipe["instructions"]))
    assert update_payload['name'] == temp_recipe["name"]
    assert update_payload['instructions'] == temp_recipe["instructions"]

def test_get_by_id_existing_recipe(db_recipe):
    get_by_id_payload = recipeDAO.get_by_id(db_recipe["id"])
    assert get_by_id_payload['id'] == db_recipe["id"]

def test_get_by_id_missing_recipe():
    get_by_id_payload = recipeDAO.get_by_id("non_existent_id")
    assert get_by_id_payload['error'] == "Recipe not found"

def test_delete_existing_recipe(db_recipe):
    _ = recipeDAO.delete(db_recipe["id"])
    get_by_id_payload = recipeDAO.get_by_id(db_recipe["id"])
    assert get_by_id_payload['error'] == "Recipe not found"

def test_delete_missing_recipe(db_recipe):
    _ = recipeDAO.delete(db_recipe["id"])
    get_by_id_payload = recipeDAO.get_by_id(db_recipe["id"])
    assert get_by_id_payload['error'] == "Recipe not found"

def test_get_by_user_id(db_user, db_recipe):
    retrieved_recipe = recipeDAO.get_by_user_id(db_user["id"])
    assert len(retrieved_recipe) == 1
    assert retrieved_recipe[0]['name'] == db_recipe['name']
    assert retrieved_recipe[0]['instructions'] == db_recipe['instructions']
    assert retrieved_recipe[0]['id'] == db_recipe['id']

def test_get_by_user_and_id(db_user, db_recipe):
    retrieved_recipe = recipeDAO.get_by_user_and_id(db_user["id"], db_recipe["id"])
    assert retrieved_recipe['id'] == db_recipe["id"]
    assert retrieved_recipe['name'] == db_recipe['name']
    assert retrieved_recipe['instructions'] == db_recipe['instructions']
    assert retrieved_recipe['user_id'] == db_user['id']