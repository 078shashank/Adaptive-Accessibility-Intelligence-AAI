"""Dependency Injection helpers"""
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from app.config import settings
from app.database import get_db
from app.models import User


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency: Get current authenticated user from JWT token in Authorization header
    
    Args:
        authorization: Bearer token from Authorization header
        db: Database session
        
    Returns:
        User model
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.split(" ")[1]
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency: Optionally get current user from JWT token (returns None if no token)
    
    Args:
        authorization: Bearer token from Authorization header
        db: Database session
        
    Returns:
        User model or None
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None  # Return None instead of raising exception
    
    token = authorization.split(" ")[1]
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
    
    user = db.query(User).filter(User.email == email).first()
    return user


def create_access_token(email: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    
    Args:
        email: User email
        expires_delta: Token expiration time
        
    Returns:
        JWT token string
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": email, "exp": expire}
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
