from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from backend.app.dao.user import authdao
from backend.app.schemas.user import UserCreate, Token

auth_router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


@auth_router.post(
    "/register",
    response_model=Token,
    tags=["Authentication"],
    responses={200: {"model": Token}, 400: {"model": str}},
)
async def register(request: RegisterRequest) -> dict:
    dao = authdao
    user_create = UserCreate(
        email=request.email, password=request.password, name=request.name
    )
    user = dao.register(user_create)
    if "error" in user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=user["error"]
        )

    token = dao.authenticate(request.email, request.password)
    if "error" in token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=token["error"]
        )
    return token


@auth_router.post(
    "/login",
    response_model=Token,
    tags=["Authentication"],
    responses={200: {"model": Token}, 401: {"model": str}},
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    dao = authdao
    token = dao.authenticate(form_data.username, form_data.password)
    if "error" in token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    return token
