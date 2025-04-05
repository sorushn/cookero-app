import pytest
from backend.app.settings import Settings
from backend.app.core.db import get_session
from backend.app.dao.recipe import recipeDAO
from backend.app.schemas.recipe import RecipeCreate
from backend.app.core.db import driver
from backend.app.dao.user import authdao
from backend.app.schemas.user import UserCreate
from loguru import logger
from backend.app.main import app
from backend.app.dependencies.auth import get_current_user_id

@pytest.fixture
def settings():
    return Settings("..//settings.ini")

@pytest.fixture
def session(settings):
    with get_session() as session:
        yield session
        session.run("MATCH (n) DETACH DELETE n")

@pytest.fixture(scope="function")
def temp_user():
    user = {
        "email": "test@example.com",
        "password": "testpassword",
        "name": "Test User"
    }
    yield user
@pytest.fixture(scope="function")
def db_user(temp_user):
    db_user = authdao.register(UserCreate(**temp_user))
    if isinstance(db_user, dict) and "error" in db_user:
        logger.warning(f"Failed to register user: {db_user['error']}")
        db_user = authdao.get_by_email(temp_user["email"])
        yield db_user
    else:
        yield db_user
        driver.execute_query("MATCH (u:User {email: $email}) DETACH DELETE u", email=temp_user["email"])

@pytest.fixture(scope="function")
def db_recipe(db_user):
    recipe = {
        "name": "Test Recipe",
        "instructions": "Test Instructions",
        "user_id": db_user["id"]
    }
    recipe = recipeDAO.create(RecipeCreate(**recipe))
    logger.debug(recipe)
    yield recipe
    driver.execute_query("MATCH (r:Recipe {id: $id}) DETACH DELETE r", id=recipe["id"])

@pytest.fixture(scope="function")
def temp_recipe(db_user):
    recipe = {
        "name": "Test Recipe",
        "instructions": "Test Instructions",
        "user_id": db_user["id"]
    }
    yield recipe
    driver.execute_query("MATCH (r:Recipe {name: $name}) DETACH DELETE r", name=recipe["name"])
