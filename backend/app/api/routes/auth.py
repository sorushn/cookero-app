from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.app.dao.user import AuthDAO
from backend.app.settings import settings

auth_router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

@auth_router.post("/register")
def register(request: RegisterRequest) -> dict:
    dao = AuthDAO(jwt_secret=settings.get("security", "SECRET_KEY"))
    return dao.register(request.email, request.password, request.name)

@auth_router.post("/login")
def login(request: LoginRequest) -> dict:
    dao = AuthDAO(jwt_secret=settings.get("security", "SECRET_KEY"))
    token = dao.authenticate(request.email, request.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return token