from fastapi import APIRouter
from loguru import logger

from backend.app.dao.recipe import recipeDAO
from backend.app.schemas.recipe import RecipeCreate
from backend.app.schemas.recipe import RecipeUpdate

recipe_router = APIRouter()


@recipe_router.post("/recipe")
def create_recipe(request: RecipeCreate) -> dict:
    response = recipeDAO.create(request)
    if "error" in response:
        logger.error(f"Error creating recipe: {response['error']}")
        return response
    return response

@recipe_router.get("/recipe/{id}")
def get_recipe(id: str) -> dict:
    response = recipeDAO.get_by_id(id)
    if "error" in response:
        logger.error(f"Error getting recipe: {response['error']}")
        return response
    return response

@recipe_router.put("/recipe/{id}")
def update_recipe(id: str, request: RecipeUpdate) -> dict:
    response = recipeDAO.update(request)
    if "error" in response:
        logger.error(f"Error updating recipe: {response['error']}")
        return response
    return response

@recipe_router.delete("/recipe/{id}")
def delete_recipe(id: str) -> dict:
    response = recipeDAO.delete(id)
    if "error" in response:
        logger.error(f"Error deleting recipe: {response['error']}")
        return response
    return {"id": id}

@recipe_router.get("/recipes/{user_id}")
def get_recipes(user_id: str) -> list[dict]:
    response = recipeDAO.get_by_user_id(user_id)
    if "error" in response:
        logger.error(f"Error getting recipes for user: {response['error']}")
        return response
    return response