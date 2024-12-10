# schemas/publication_schema.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.schemas.user_schema import UserBase

class Page(BaseModel):
    id: int
    url: str

class TagSchema(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]

class UserDetailSchema(BaseModel):
    name: str
    lastName: str
    mail: EmailStr
    bio: Optional[str] = None
    degreeTitle: str

class PublicationBase(BaseModel):
    title: str
    content: str
    tags: List[int]

class PublicationCreate(PublicationBase):
    user_id: UUID
    page_id: int

class PublicationUpdate(PublicationBase):
    page_id: int
    pass

class PublicationResponse(PublicationBase):
    id: UUID
    date: datetime
    user_id: UUID
    user: UserBase
    page: Page
    tags: List[TagSchema]
    page_id: int
    likes_count: int = 0
    dislikes_count: int = 0
    
    class Config:
        orm_mode = True