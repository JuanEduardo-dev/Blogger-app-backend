# services/user_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.degree import Degree
from ..models.user import User
from ..schemas.user_schema import UserPublicResponse, UserUpdate
import os

class UserService:
    def __init__(self, db: Session):
        self.db = db


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_info(self, user_id: str):
        try:
            user_with_degree = (
                self.db.query(User, Degree)
                .join(Degree, User.degreeId == Degree.id)
                .filter(User.id == user_id)
                .first()
            )

            if not user_with_degree:
                raise HTTPException(status_code=404, detail="User not found")

            user, degree = user_with_degree

            user_info = UserPublicResponse (
                name=user.name,
                lastName=user.lastName,
                mail=user.mail,
                bio=user.bio,
                degreeTitle=degree.title
            )

            return user_info
        
        except Exception as e:
            print(f"Error retrieving user info: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    
    def update_user(self, user_id: str, user_update: UserUpdate):
        """
        Update user information based on user ID
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update user fields if provided
        if user_update.name:
            user.name = user_update.name
        if user_update.lastName:
            user.lastName = user_update.lastName
        if user_update.bio is not None:
            user.bio = user_update.bio
        if user_update.degreeId:
            user.degreeId = user_update.degreeId
        
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def delete_user(self, user_id: str):
        """
        Delete user based on user ID
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        try:
            self.db.delete(user)
            self.db.commit()
            return {"message": "User deleted successfully"}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
            