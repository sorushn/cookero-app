from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from backend.app.core.security import decode_jwt_token
from backend.app.dao.user import authdao

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class TokenData(BaseModel):
    user_id: str


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependency to get the current user ID from a JWT token.
    
    Args:
        token: JWT token extracted from the Authorization header
        
    Returns:
        The user ID if the token is valid
        
    Raises:
        HTTPException: If the token is invalid or expired
    """
    user_id = decode_jwt_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


async def get_current_user(user_id: str = Depends(get_current_user_id)):
    """
    Dependency to get the current user from the database.
    
    Args:
        user_id: User ID extracted from the JWT token
        
    Returns:
        The user details if the user exists
        
    Raises:
        HTTPException: If the user does not exist
    """
    user = authdao.get_by_id(user_id)
    if "error" in user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
