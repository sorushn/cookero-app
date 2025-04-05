from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    token: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
