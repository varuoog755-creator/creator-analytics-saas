from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.core.config import settings
from app.api.auth import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to get current authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = decode_token(token)
    
    if token_data is None or token_data.email is None:
        raise credentials_exception
    
    # In production, fetch user from database
    user = {
        "id": token_data.user_id,
        "email": token_data.email,
        "is_active": True
    }
    
    return user


async def get_current_active_user(current_user = Depends(get_current_user)):
    """
    Get current active user.
    """
    if not current_user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
