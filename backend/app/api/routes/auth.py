from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.app.dao.user import authdao

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
    dao = authdao
    dao.register(request)
    token = dao.authenticate(request.email, request.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error Registering User")
    return token

@auth_router.post("/login")
def login(request: LoginRequest) -> dict:
    dao = authdao
    token = dao.authenticate(request.email, request.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return token