from uuid import uuid4

from backend.app.core.db import get_session, driver
from backend.app.core.security import create_access_token, get_password_hash, verify_password, decode_jwt_token
from backend.app.settings import settings
from backend.app.schemas.recipe import RecipeCreate
class RecipeDAO:
    def __init__(self):
        raise NotImplementedError

    def create(self, request: RecipeCreate):
        raise NotImplementedError