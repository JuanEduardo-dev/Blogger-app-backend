# schemas/user_schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    name: str
    lastName: str
    mail: EmailStr
    bio: Optional[str] = None
    degreeId: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    lastName: Optional[str] = None
    bio: Optional[str] = None
    degreeId: Optional[int] = None

class UserResponse(UserBase):
    id: str
    name: str
    lastName: str
    mail: str
    bio: Optional[str] = None
    degreeId: int
    degreeTitle: str

class UserPublicResponse(BaseModel):
    name: str
    lastName: str
    mail: EmailStr
    bio: Optional[str] = None
    degreeTitle: Optional[str] = None
