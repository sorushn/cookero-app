from uuid import uuid4

from loguru import logger
from backend.app.core.db import driver
from backend.app.schemas.recipe import RecipeCreate, RecipeUpdate


class RecipeDAO:
    def __init__(self):
        pass

    def create(self, request: RecipeCreate):
        try:
            records, _, _ = driver.execute_query(
                """
                CREATE (r:Recipe {
                    name: $name,
                    instructions: $instructions,
                    user_id: $user_id,
                    id: $id
                })
                RETURN r
                """,
                name=request.name,
                instructions=request.instructions,
                user_id=request.user_id,
                id=str(uuid4()),
            )
            logger.debug(f"Successfully created recipe with name {request.name}")
            return records[0]["r"]
        except Exception as e:
            logger.error(f"Error creating recipe: {str(e)}")
            return {"error": str(e)}

    def update(self, request: RecipeUpdate):
        try:
            records, _, _ = driver.execute_query(
                """
                MATCH (r:Recipe {id: $id})
                SET r.name = $name,
                    r.instructions = $instructions
                RETURN r
                """,
                id=request.id,
                name=request.name,
                instructions=request.instructions,
            )
            logger.debug(f"Successfully updated recipe with id {request.id}")
            return records[0]["r"]
        except Exception as e:
            logger.error(f"Error updating recipe: {str(e)}")
            return {"error": str(e)}

    def get_by_user_id(self, user_id: str):
        try:
            records, _, _ = driver.execute_query(
                """
                MATCH (r:Recipe {user_id: $user_id})
                RETURN r
                """,
                user_id=user_id,
            )
            if not records:
                logger.debug(f"No recipes found for user with id {user_id}")
                return []
            logger.debug(f"Successfully retrieved recipes for user with id {user_id}")
            return [record["r"] for record in records]
        except Exception as e:
            logger.error(f"Error retrieving recipes for user: {str(e)}")
            return {"error": str(e)}

    def delete(self, id: str):
        try:
            records, _, _ = driver.execute_query(
                """
                MATCH (r:Recipe {id: $id})
                DELETE r
                RETURN r
                """,
                id=id,
            )
            logger.debug(f"Successfully deleted recipe with id {id}")
            return records[0]["r"]
        except Exception as e:
            logger.error(f"Error deleting recipe: {str(e)}")
            return {"error": str(e)}

    def get_by_id(self, id: str):
        try:
            records, _, _ = driver.execute_query(
                """
                MATCH (r:Recipe {id: $id})
                RETURN r
                """,
                id=id,
            )
            if records:
                logger.debug(f"Successfully retrieved recipe with id {id}")
                return records[0]["r"]
            else:
                return {"error": "Recipe not found"}
        except Exception as e:
            logger.error(f"Error retrieving recipe: {str(e)}")
            return {"error": str(e)}

    def get_by_user_and_id(self, user_id: str, id: str):
        try:
            records, _, _ = driver.execute_query(
                """
                MATCH (r:Recipe {id: $id})
                WHERE r.user_id = $user_id
                RETURN r
                """,
                id=id,
                user_id=user_id,
            )
            if records:
                logger.debug(f"Successfully retrieved recipe with id {id}")
                return records[0]["r"]
            else:
                return {"error": "Recipe not found"}
        except Exception as e:
            logger.error(f"Error retrieving recipe: {str(e)}")
            return {"error": str(e)}


recipeDAO = RecipeDAO()
