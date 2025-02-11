from datetime import datetime, timedelta, timezone
from typing import Any, Union

import jwt
from passlib.context import CryptContext

from backend.app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.get("security", "ALGORITHM")
SECRET_KEY = settings.get("security", "SECRET_KEY")
EXPIRE_MINUTES = int(settings.get("security", "EXPIRE_MINUTES"))

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = timedelta(minutes=EXPIRE_MINUTES)
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)