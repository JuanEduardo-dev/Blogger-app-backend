from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class ReactionType(str, Enum):
    LIKE = 'like'
    DISLIKE = 'dislike'

class ReactionCreate(BaseModel):
    id_user: UUID
    id_publication: UUID
    type: ReactionType

class ReactionResponse(BaseModel):
    id_user: UUID
    id_publication: UUID
    date: datetime
    type: ReactionType

class PublicationReactionCountResponse(BaseModel):
    likes_count: int = 0
    dislikes_count: int = 0