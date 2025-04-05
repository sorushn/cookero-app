from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from backend.app.dao.recipe import recipeDAO
from backend.app.schemas.recipe import RecipeCreate
from backend.app.schemas.recipe import RecipeUpdate, RecipeCreateResponse
from backend.app.dependencies.auth import get_current_user_id

recipe_router = APIRouter()


@recipe_router.post("/recipe", tags=["Recipes"], responses={200: {"model": RecipeCreateResponse}, 400: {"model": str}})
async def create_recipe(request: RecipeCreate, current_user_id: str = Depends(get_current_user_id)) -> dict:
    # Set the user_id from the authenticated user
    request.user_id = current_user_id
    response = recipeDAO.create(request)
    if "error" in response:
        logger.error(f"Error creating recipe: {response['error']}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return response

@recipe_router.get("/recipe/{id}", tags=["Recipes"], responses={200: {"model": RecipeCreateResponse}, 400: {"model": str}})
async def get_recipe(id: str, current_user_id: str = Depends(get_current_user_id)) -> dict:
    response = recipeDAO.get_by_id(id)
    if "error" in response:
        logger.error(f"Error getting recipe: {response['error']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response["error"])
    
    # Check if the recipe belongs to the authenticated user
    if response.get("user_id") != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this recipe"
        )
    return response

@recipe_router.put("/recipe/{id}", tags=["Recipes"], responses={200: {"model": RecipeCreateResponse}, 400: {"model": str}})
async def update_recipe(id: str, request: RecipeUpdate, current_user_id: str = Depends(get_current_user_id)) -> dict:
    # Check if the recipe belongs to the current user before updating
    recipe = recipeDAO.get_by_id(id)
    if "error" in recipe:
        logger.error(f"Error getting recipe: {recipe['error']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=recipe["error"])
    
    if recipe.get("user_id") != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this recipe"
        )
    
    request.id = id  # Ensure the ID is set correctly
    response = recipeDAO.update(request)
    if "error" in response:
        logger.error(f"Error updating recipe: {response['error']}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return response

@recipe_router.delete("/recipe/{id}", tags=["Recipes"], responses={200: {"model": str}, 400: {"model": str}})
async def delete_recipe(id: str, current_user_id: str = Depends(get_current_user_id)) -> dict:
    # Check if the recipe belongs to the current user before deleting
    recipe = recipeDAO.get_by_id(id)
    if "error" in recipe:
        logger.error(f"Error getting recipe: {recipe['error']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=recipe["error"])
    
    if recipe.get("user_id") != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this recipe"
        )
    
    response = recipeDAO.delete(id)
    if "error" in response:
        logger.error(f"Error deleting recipe: {response['error']}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"id": id}

@recipe_router.get("/recipes", tags=["Recipes"], responses={200: {"model": list[RecipeCreateResponse]}, 400: {"model": str}})
async def get_recipes(current_user_id: str = Depends(get_current_user_id)) -> list[dict]:
    # Get recipes for the current authenticated user
    response = recipeDAO.get_by_user_id(current_user_id)
    if "error" in response:
        logger.error(f"Error getting recipes for user: {response['error']}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return response