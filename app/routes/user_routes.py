# routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional

from ..config.database import get_db
from ..schemas.user_schema import UserUpdate, UserResponse, UserPublicResponse
from ..services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.put("/me", response_model=UserResponse)
async def update_user(
    user_update: UserUpdate, 
    db: Session = Depends(get_db), 
    user_id: Optional[str] = Header(None)
):
    """
    Update current user's information
    Requires user ID for authentication
    """
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID is required")
    
    service = UserService(db)
    return service.update_user(user_id, user_update)

@router.get("/me", response_model=UserPublicResponse)
async def get_user_info(
    db: Session = Depends(get_db), 
    user_id: Optional[str] = Header(None)
):
    """
    Get current user's information
    Requires user ID for authentication
    """
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID is required")

    service = UserService(db)
    return service.get_user_info(user_id)

@router.delete("/me")
async def delete_user(
    db: Session = Depends(get_db), 
    user_id: Optional[str] = Header(None)
):
    """
    Delete current user
    Requires user ID for authentication
    """
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID is required")
    
    service = UserService(db)
    return service.delete_user(user_id)